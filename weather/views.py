from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import DailyForecastWeather
from data.models import City
from datetime import datetime, timedelta
from django.utils import timezone


def from_utc_to_local(few_day, timezone_offset):
    few_day.datetime_utc = few_day.datetime_utc + timedelta(seconds=timezone_offset)
    few_day.datetime_utc = few_day.datetime_utc.replace(tzinfo=timezone.utc)
    return few_day


def forecast_7days(request, name):
    city = get_object_or_404(City, name_en=name)
    timezone_offset = city.time_zone.rawOffset

    now_utc = datetime.now(tz=timezone.utc)
    # В forecast_local tz=UTC во избежании неопределенности django. Формально, tz != UTC
    forecast_local = datetime(day=now_utc.day, month=now_utc.month, year=now_utc.year, tzinfo=
                              timezone.utc) + timedelta(days=1)
    forecast_utc = forecast_local - timedelta(seconds=timezone_offset)

    # Вычисляем значения отступов для запросов к БД. Время в UTC
    first_day = forecast_utc
    second_day = first_day + timedelta(days=1)
    third_day = first_day + timedelta(days=2)
    four_day = first_day + timedelta(days=3)
    five_day = first_day + timedelta(days=4)
    six_day = first_day + timedelta(days=5)
    seven_day = first_day + timedelta(days=6)

    # Получаям информацию по дням
    first_day = DailyForecastWeather.objects.get(datetime_utc=first_day)
    second_day = DailyForecastWeather.objects.get(datetime_utc=second_day)
    third_day = DailyForecastWeather.objects.get(datetime_utc=third_day)
    four_day = DailyForecastWeather.objects.get(datetime_utc=four_day)
    five_day = DailyForecastWeather.objects.get(datetime_utc=five_day)
    six_day = DailyForecastWeather.objects.get(datetime_utc=six_day)
    seven_day = DailyForecastWeather.objects.get(datetime_utc=seven_day)

    # Меняем данные для корректного вывода. Время местное
    first_day = from_utc_to_local(few_day=first_day, timezone_offset=timezone_offset)
    second_day = from_utc_to_local(few_day=second_day, timezone_offset=timezone_offset)
    third_day = from_utc_to_local(few_day=third_day, timezone_offset=timezone_offset)
    four_day = from_utc_to_local(few_day=four_day, timezone_offset=timezone_offset)
    five_day = from_utc_to_local(few_day=five_day, timezone_offset=timezone_offset)
    six_day = from_utc_to_local(few_day=six_day, timezone_offset=timezone_offset)
    seven_day = from_utc_to_local(few_day=seven_day, timezone_offset=timezone_offset)

    all_days = first_day, second_day, third_day, four_day, five_day, six_day, seven_day

    return render(request, 'weather/forecast_7_days.html', {
        'city': city,
        'all_days': all_days,
    })


def forecast_for_day(request, name, day, month, year):
    city = get_object_or_404(City, name_en=name)
    try:
        now_utc = datetime(day=day, month=month, year=year, tzinfo=timezone.utc)
    except ValueError:
        raise Http404
    timezone_offset = city.time_zone.rawOffset
    now_local = now_utc - timedelta(seconds=timezone_offset)
    report = get_object_or_404(DailyForecastWeather, datetime_utc=now_local)
    report = from_utc_to_local(few_day=report, timezone_offset=timezone_offset)

    return render(request, 'weather/forecast_for_day.html', {
        'city': city,
        'report': report,
    })
