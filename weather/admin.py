from django.contrib import admin
from .models import HourlyWeather


@admin.register(HourlyWeather)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['city', 'date', 'icon_name', 'temperature']
