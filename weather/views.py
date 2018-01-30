from django.shortcuts import render
from .models import HourlyForecastWeather
from data.models import City


def forecast_7days(request, name):
    city = City.objects.get(name_en=name)
    all_hours = HourlyForecastWeather.objects.filter(city__name_en=name)
    return render(request, 'weather/forecast_7_days.html', {
        'city': city,
        'all_hours': all_hours,
    })
