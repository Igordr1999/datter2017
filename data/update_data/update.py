from data.models import Country, City, Region, SubRegion, Valuta, Language, TimeZone
from currency.models import Valuta, ValutaValue
from weather.models import HourlyWeather

from datetime import datetime
from django.utils import timezone
import pytz
from darksky import forecast


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
    my_precip_type = "NO DATA"
    my_visibility = 30

    def __init__(self, city_alpha3):
        self.city_alpha3 = city_alpha3

    def get_hourly_weather(self):
        city = City.objects.get(alpha3=self.city_alpha3)
        lat = city.latitude
        lon = city.longitude
        weather = forecast(key=self.WEATHER_API_KEY, latitude=lat, longitude=lon, lang=self.WEATHER_LANG,
                           units=self.WEATHER_UNITS)
        weather.refresh(units='si', extend='hourly')  # Получаем 24*7 строк, а не 24*3 по дефолту
        self.save_hourly_weather(weather=weather, city=city)

    def give_default_value(self, key):
        if hasattr(key, 'precipType'):
            self.my_precip_type = key.precipType

        if hasattr(key, 'visibility'):
            self.my_visibility = key.visibility

    def save_hourly_weather(self, weather, city):
        for i in weather.hourly:
            my_date = timezone.datetime.utcfromtimestamp(i.time).astimezone(timezone.utc)
            # Присваиваем дефолтные значения необязательным атрибутам (precipType и visibility)
            self.give_default_value(i)

            # добавляем или обновляем объект в БД
            new_data = {'response_text': weather.hourly._data,
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
            HourlyWeather.objects.update_or_create(
                city=city,
                date=my_date,
                defaults=new_data,
            )
