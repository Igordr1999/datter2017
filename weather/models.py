from django.db import models
from data.models import City


class DailyForecastWeather(models.Model):
    raw_response_datetime = models.DateTimeField(verbose_name="Дата и время запроса", auto_now_add=True)
    raw_response = models.CharField(max_length=2000, verbose_name="Ответ сервера")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")

    datetime_utc = models.DateTimeField(verbose_name="Дата и время по UTC")  # original name = time
    summary = models.CharField(verbose_name="Текстовое описание", max_length=500)
    icon_name = models.CharField(verbose_name="Название иконки", max_length=100)

    sunriseTime = models.DateTimeField(verbose_name="Время восхода")
    sunsetTime = models.DateTimeField(verbose_name="Время заката")
    moonPhase = models.FloatField(verbose_name="Фаза Луны")

    precipIntensity = models.FloatField(verbose_name="Интенсивность осадков")
    precipProbability = models.FloatField(verbose_name="Вероятность осадков")
    precipType = models.CharField(verbose_name="Тип осадков", max_length=100, default="NO DATA")

    temperatureHigh = models.FloatField(verbose_name="Наибольшая температура")
    temperatureLow = models.FloatField(verbose_name="Наименьшая температура")
    apparentTemperatureHigh = models.FloatField(verbose_name="RealFeel max")
    apparentTemperatureLow = models.FloatField(verbose_name="RealFeel min")

    dewPoint = models.FloatField(verbose_name="Точка росы")
    humidity = models.FloatField(verbose_name="Влажность")
    pressure = models.FloatField(verbose_name="Давление")

    windSpeed = models.FloatField(verbose_name="Скорость ветра")
    windGust = models.FloatField(verbose_name="Порывы ветра")
    windBearing = models.IntegerField(verbose_name="Направление ветра")

    cloudCover = models.FloatField("Облачность")
    uvIndex = models.IntegerField(verbose_name="УВ-индекс")
    ozone = models.FloatField(verbose_name="Озон")

    def __str__(self):
        return str(self.city)

    class Meta:
        verbose_name = "Погода на день"
        verbose_name_plural = "Погода на дни"
        ordering = ["city", "datetime_utc"]


class HourlyForecastWeather(models.Model):
    raw_response_datetime = models.DateTimeField(verbose_name="Дата и время запроса", auto_now_add=True)
    raw_response = models.CharField(max_length=2000, verbose_name="Ответ сервера")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")

    datetime_utc = models.DateTimeField(verbose_name="Дата и время по UTC")  # original name = time
    summary = models.CharField(verbose_name="Текстовое описание", max_length=500)
    icon_name = models.CharField(verbose_name="Название иконки", max_length=100)

    precipIntensity = models.FloatField(verbose_name="Интенсивность осадков")
    precipProbability = models.FloatField(verbose_name="Вероятность осадков")
    precipType = models.CharField(verbose_name="Тип осадков", max_length=100, default="NO DATA")

    temperature = models.FloatField(verbose_name="Температура")
    apparentTemperature = models.FloatField(verbose_name="RealFeel температура")

    dewPoint = models.FloatField(verbose_name="Точка росы")
    humidity = models.FloatField(verbose_name="Влажность")
    pressure = models.FloatField(verbose_name="Давление")

    windSpeed = models.FloatField(verbose_name="Скорость ветра")
    windGust = models.FloatField(verbose_name="Порывы ветра")
    windBearing = models.IntegerField(verbose_name="Направление ветра")

    cloudCover = models.FloatField("Облачность")
    uvIndex = models.IntegerField(verbose_name="УВ-индекс")
    visibility = models.FloatField(verbose_name="Видимость", default=30)
    ozone = models.FloatField(verbose_name="Озон")

    def __str__(self):
        return str(self.city)

    class Meta:
        verbose_name = "Погода за час"
        verbose_name_plural = "Почасовая погода"
        ordering = ["city", "datetime_utc"]
