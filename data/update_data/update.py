from data.models import Country, City, Region, SubRegion, Valuta, Language, TimeZone
from currency.models import Valuta, ValutaValue

from datetime import datetime


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
