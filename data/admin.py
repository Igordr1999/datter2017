from django.contrib import admin
from data.models import Language, TimeZone, Region, SubRegion, Country, City


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
