from django.shortcuts import render, get_object_or_404
from .models import TimeZone, City


def time_home(request):
    Moscow = City.objects.get(alpha3="MOW")
    Kiev = City.objects.get(alpha3="KIE")
    SP = City.objects.get(alpha3="SPB")
    London = City.objects.get(alpha3="LON")
    Sydney = City.objects.get(alpha3="SYD")
    Tokyo = City.objects.get(alpha3="TOK")

    top6 = [Moscow, Kiev, SP, London, Tokyo, Sydney]
    return render(request, 'data/data_time_main.html', {
        'top6': top6,
    })


def time_city(request, name):
    info = get_object_or_404(City, name_en=name)
    return render(request, 'data/data_time_city.html', {'info': info})


def time_timezone(request, name):
    info = get_object_or_404(TimeZone, timeZoneId=name)
    return render(request, 'data/data_time_timezone.html', {'info': info})


def time_cities(request):
    info = City.objects.all()
    return render(request, 'data/data_time_cities.html', {'info': info})


def time_timezones(request):
    info = TimeZone.objects.all()
    return render(request, 'data/data_time_timezones.html', {'info': info})
