from django.contrib import admin
from .models import HourlyForecastWeather, DailyForecastWeather


@admin.register(HourlyForecastWeather)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['city', 'datetime_utc', 'icon_name', 'temperature', 'summary']


admin.site.register(DailyForecastWeather)

