from django.contrib import admin
from .models import HourlyForecastWeather


@admin.register(HourlyForecastWeather)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['city', 'datetime_utc', 'icon_name', 'temperature', 'summary']
