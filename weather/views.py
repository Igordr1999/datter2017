from django.shortcuts import render
from .models import HourlyWeather
from data.models import City


def forecast_7days(request, name):
    city = City.objects.get(name_en=name)
    all_hours = HourlyWeather.objects.filter(city__name_en=name)
    return render(request, 'weather/forecast_10_days.html', {
        'city': city,
        'all_hours': all_hours,
    })
