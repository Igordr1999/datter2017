from django.contrib import admin
from .models import HourlyForecastWeather, DailyForecastWeather


@admin.register(HourlyForecastWeather)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['city', 'datetime_utc', 'icon_name', 'temperature', 'summary']


@admin.register(DailyForecastWeather)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['city', 'datetime_utc', 'icon_name', 'temperatureHigh', 'temperatureLow', 'summary',
                    'sunriseTime', 'sunsetTime', 'moonPhase']

