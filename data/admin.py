from django.contrib import admin
from data.models import \
    Language, TimeZone, Region, SubRegion, Country, City, Alliance, AircraftType, Aircraft, Airport, Airline


@admin.register(Language)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'name_en', 'alpha2', 'alpha3', 'numeric']


@admin.register(TimeZone)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['timeZoneId', 'timeZoneName', 'rawOffset', 'dstOffset', 'is_primary']


@admin.register(Region)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'name_en', 'alpha2', 'numeric']


@admin.register(SubRegion)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['region', 'name_ru', 'name_en', 'alpha2', 'numeric']


@admin.register(Country)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'name_en', 'alpha2', 'alpha3', 'numeric', 'sub_region', 'currency', 'language']


@admin.register(City)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['country', 'name_ru', 'name_en', 'alpha3', 'latitude', 'longitude', 'is_capital', 'time_zone']


@admin.register(Alliance)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'logo']


@admin.register(Airport)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'name_en', 'iata_code', 'icao_code', 'latitude', 'longitude', 'altitude', 'country',
                    'city']


@admin.register(Airline)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'name_en', 'iata_code', 'icao_code', 'alliance']


@admin.register(AircraftType)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['model_ru', 'model_en', 'icao_code', 'iata_code']


@admin.register(Aircraft)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['model', 'modification', 'msn', 'registration', 'airline', 'create_date', 'status', 'note']
