from data.models import Country, City, Region, SubRegion, Valuta, Language, TimeZone
from currency.models import Valuta, ValutaValue
from weather.models import HourlyForecastWeather, DailyForecastWeather

from datetime import datetime, timedelta, date
from django.utils import timezone  # именно отсюда импорт
import pytz
from darksky import forecast
from django.db.models import Avg, Max, Min


class Update(object):
    @staticmethod
    def add_country(name_ru, name_en, full_name_ru, full_name_en, alpha2, alpha3, numeric, area, population,
                    sub_region_alpha2, currency_char_code, language_alpha2):
        my_sub_region = SubRegion.objects.get(alpha2=sub_region_alpha2)
        my_currency = Valuta.objects.get(char_code=currency_char_code)
        my_language = Language.objects.get(alpha2=language_alpha2)
        Country.objects.create(name_ru=name_ru, name_en=name_en, full_name_ru=full_name_ru,
                               full_name_en=full_name_en, alpha2=alpha2, alpha3=alpha3, numeric=numeric,
                               area=area, population=population, sub_region=my_sub_region, currency=my_currency,
                               language=my_language)

    @staticmethod
    def add_city(country_alpha2, name_ru, name_en, alpha3, latitude, longitude, is_cap,
                 area, population, time_zone_timeZoneId):
        my_country = Country.objects.get(alpha2=country_alpha2)
        my_time_zone = TimeZone.objects.get(timeZoneId=time_zone_timeZoneId)
        City.objects.create(country=my_country, name_ru=name_ru, name_en=name_en, alpha3=alpha3,
                            latitude=latitude, longitude=longitude, is_capital=is_cap,
                            area=area, population=population, time_zone=my_time_zone)

    @staticmethod
    def add_sub_region(region_code_alpha2, name_ru, name_en, alpha2, numeric):
        my_region = Region.objects.get(alpha2=region_code_alpha2)
        SubRegion.objects.create(region=my_region, name_ru=name_ru, name_en=name_en, alpha2=alpha2, numeric=numeric)

    @staticmethod
    def add_region(name_ru, name_en, alpha2, numeric):
        Region.objects.create(name_ru=name_ru, name_en=name_en, alpha2=alpha2, numeric=numeric)

    @staticmethod
    def add_time_zone(zone_id, zone_name, raw_offset, dst_offset, is_primary):
        TimeZone.objects.create(timeZoneId=zone_id, timeZoneName=zone_name, rawOffset=raw_offset, dstOffset=dst_offset,
                                is_primary=is_primary)

    @staticmethod
    def add_language(name_ru, name_en, alpha2, alpha3, numeric):
        Language.objects.create(name_ru=name_ru, name_en=name_en,
                                alpha2=alpha2, alpha3=alpha3, numeric=numeric)

    @staticmethod
    def add_currency_valuta(name_ru, name_en, char_code, num_code, nominal, description, popular):
        Valuta.objects.create(name_ru=name_ru, name_en=name_en, char_code=char_code, num_code=num_code,
                              nominal=nominal, description=description, popular=popular)

    @staticmethod
    def add_currency_value(valuta, day, month, year, value):
        my_date = datetime(day=day, month=month, year=year)
        my_valuta = Valuta.objects.get(char_code=valuta)
        ValutaValue.objects.create(valuta=my_valuta, date=my_date, value=value)


class ForecastApiRequest(object):
    WEATHER_API_KEY = "98e750a215fca2aa271b64eb3fde5c7c"
    WEATHER_LANG = "ru"
    WEATHER_UNITS = "si"
    city_alpha3 = ""
    city = ""
    my_precip_type = "NO DATA"
    my_visibility = 30

    def __init__(self, city_alpha3):
        self.city_alpha3 = city_alpha3
        self.city = City.objects.get(alpha3=self.city_alpha3)

    def get_all_weather(self):
        lat = self.city.latitude
        lon = self.city.longitude
        weather = forecast(key=self.WEATHER_API_KEY, latitude=lat, longitude=lon, lang=self.WEATHER_LANG,
                           units=self.WEATHER_UNITS)
        weather.refresh(units='si', extend='hourly', lang='ru')  # Получаем 24*7 строк, а не 24*3 по дефолту
        self.save_hourly_weather(weather=weather, city=self.city)
        self.save_daily_weather(weather=weather, city=self.city)

    def give_default_value_hourly(self, key):
        if hasattr(key, 'precipType'):
            self.my_precip_type = key.precipType

        if hasattr(key, 'visibility'):
            self.my_visibility = key.visibility

    def give_default_value_daily(self, key):
        if hasattr(key, 'precipType'):
            self.my_precip_type = key.precipType

    def save_hourly_weather(self, weather, city):
        for i in weather.hourly:
            my_date = timezone.datetime.utcfromtimestamp(i.time)
            my_datetime_utc = my_date.replace(tzinfo=timezone.utc)

            # Присваиваем дефолтные значения необязательным атрибутам (precipType и visibility)
            self.give_default_value_hourly(i)

            # добавляем или обновляем объект в БД
            new_data = {
                        'summary': i.summary,
                        'icon_name': i.icon,

                        'precipIntensity': i.precipIntensity,
                        'precipProbability': i.precipProbability,
                        'precipType': self.my_precip_type,

                        'temperature': i.temperature,
                        'apparentTemperature': i.apparentTemperature,

                        'dewPoint': i.dewPoint,
                        'humidity': i.humidity,
                        'pressure': i.pressure,

                        'windSpeed': i.windSpeed,
                        'windGust': i.windGust,
                        'windBearing': i.windBearing,

                        'cloudCover': i.cloudCover,
                        'uvIndex': i.uvIndex,
                        'visibility': self.my_visibility,
                        'ozone': i.ozone,
                        }
            HourlyForecastWeather.objects.update_or_create(
                city=city,
                datetime_utc=my_datetime_utc,
                defaults=new_data,
            )

    def save_daily_weather(self, weather, city):
        for i in weather.daily:
            my_datetime_utc = timezone.datetime.utcfromtimestamp(i.time).replace(tzinfo=timezone.utc)
            my_sunrise_time = timezone.datetime.utcfromtimestamp(i.sunriseTime).replace(tzinfo=timezone.utc)
            my_sunset_time = timezone.datetime.utcfromtimestamp(i.sunsetTime).replace(tzinfo=timezone.utc)

            # Получаем ссылки на периоды этого дня (часы: 0-3-6-9-12-15-18-21)
            my_list = self.research_daily_forecast(my_date=my_datetime_utc)

            # Присваиваем дефолтные значения необязательным атрибутам (precipType и visibility)
            self.give_default_value_daily(i)

            # добавляем или обновляем объект в БД
            new_data = {
                        'summary': i.summary,
                        'icon_name': i.icon,

                        'sunriseTime': my_sunrise_time,
                        'sunsetTime': my_sunset_time,
                        'moonPhase': i.moonPhase,

                        'precipIntensity': i.precipIntensity,
                        'precipProbability': i.precipProbability,
                        'precipType': self.my_precip_type,

                        'temperatureMax': i.temperatureMax,
                        'temperatureMin': i.temperatureMin,
                        'apparentTemperatureHigh': i.apparentTemperatureHigh,
                        'apparentTemperatureLow': i.apparentTemperatureLow,

                        'dewPoint': i.dewPoint,
                        'humidity': i.humidity,
                        'pressure': i.pressure,

                        'windSpeed': i.windSpeed,
                        'windGust': i.windGust,
                        'windBearing': i.windBearing,

                        'cloudCover': i.cloudCover,
                        'uvIndex': i.uvIndex,
                        'ozone': i.ozone,

                        'situation_0': my_list[0],
                        'situation_3': my_list[1],
                        'situation_6': my_list[2],
                        'situation_9': my_list[3],
                        'situation_12': my_list[4],
                        'situation_15': my_list[5],
                        'situation_18': my_list[6],
                        'situation_21': my_list[7],
                        }
            DailyForecastWeather.objects.update_or_create(
                city=city,
                datetime_utc=my_datetime_utc,
                defaults=new_data,
            )

    def get_or_last(self, datetime_utc):
        hourly_forecast = HourlyForecastWeather.objects.filter(city=self.city)
        try:
            return HourlyForecastWeather.objects.get(city=self.city, datetime_utc=datetime_utc)
        except HourlyForecastWeather.DoesNotExist:
            return hourly_forecast.last()

    def research_daily_forecast(self, my_date):
        timezone_offset = self.city.time_zone.rawOffset
        today = my_date + timedelta(days=1)
        date_offset = timedelta(seconds=timezone_offset)

        # time_xx - нужное время для вывода, XX - часы по UTC
        time_0 = today.replace(hour=0) - date_offset
        time_3 = today.replace(hour=3) - date_offset
        time_6 = today.replace(hour=6) - date_offset
        time_9 = today.replace(hour=9) - date_offset
        time_12 = today.replace(hour=12) - date_offset
        time_15 = today.replace(hour=15) - date_offset
        time_18 = today.replace(hour=18) - date_offset
        time_21 = today.replace(hour=21) - date_offset

        # Если данных пока не хватает для последних часов, заполняем их последний известным часом
        info_0 = self.get_or_last(time_0)
        info_3 = self.get_or_last(time_3)
        info_6 = self.get_or_last(time_6)
        info_9 = self.get_or_last(time_9)
        info_12 = self.get_or_last(time_12)
        info_15 = self.get_or_last(time_15)
        info_18 = self.get_or_last(time_18)
        info_21 = self.get_or_last(time_21)

        return info_0, info_3, info_6, info_9, info_12, info_15, info_18, info_21

    def get_today_local(self, city):
        now_utc = datetime.now(tz=timezone.utc)
        timezone_offset = city.time_zone.rawOffset
        now_local = now_utc - timedelta(seconds=timezone_offset)
        return now_local

    def get_7_coming_day(self, city):
        first_day = self.get_today_local(city=city)
        second_day = first_day + timedelta(days=1)
        third_day = first_day + timedelta(days=2)
        four_day = first_day + timedelta(days=3)
        five_day = first_day + timedelta(days=4)
        six_day = first_day + timedelta(days=5)
        seven_day = first_day + timedelta(days=6)
        return first_day, second_day, third_day, four_day, five_day, six_day, seven_day
