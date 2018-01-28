from django.db import models
from data.models import City

'''
class Daily(models.Model):
    response_datetime = models.DateTimeField(verbose_name="Дата и время запроса", auto_now_add=True)
    response_text = models.CharField(max_length=2000, verbose_name="Полный ответ")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")

    date = models.DateField(verbose_name="Дата", auto_now_add=True)  # original name = time
    summary = models.TextField(verbose_name="Резюме", max_length=500, default="qq")
    icon_name = models.CharField(verbose_name="Название иконки", max_length=100, default='qq')

    sunriseTime = models.DateTimeField(verbose_name="Время восхода")
    sunsetTime = models.DateTimeField(verbose_name="Время заката")
    moonPhase = models.FloatField(verbose_name="Фаза Луны")
    
    precipIntensity = models.FloatField(verbose_name="Интенсивность осадков")
    precipIntensityMax = models.FloatField(verbose_name="Интенсивность осадков (max, value)")
    precipIntensityMaxTime = models.DateTimeField(verbose_name="Интенсивность осадков (max, time)")
    precipProbability = models.FloatField(verbose_name="Вероятность осадков")
    precipType = models.CharField(verbose_name="Тип осадков", max_length=100)

    temperatureHigh = models.FloatField(verbose_name="Наибольшая температура (знач)")
    temperatureHighTime = models.DateTimeField(verbose_name="Наибольшая температура (время)")
    temperatureLow = models.FloatField(models.FloatField(verbose_name="Наименьшая температура (знач)"))
    temperatureLowTime = models.DateTimeField(verbose_name="Наименьшая температура (время)")

    apparentTemperatureHigh = models.FloatField(verbose_name="RealFeel (max, value)")
    apparentTemperatureHighTime = models.TimeField(verbose_name="RealFeel (max, time)")
    apparentTemperatureLow = models.FloatField(verbose_name="RealFeel (min, value)")
    apparentTemperatureLowTime = models.TimeField(verbose_name="RealFeel (min, time)")

    dewPoint = models.FloatField(verbose_name="Точка росы")
    humidity = models.FloatField(verbose_name="Влажность")
    pressure = models.FloatField(verbose_name="Давление")

    windSpeed = models.FloatField(verbose_name="Скорость ветра")
    windGust = models.FloatField(verbose_name="Порывы ветра")
    windGustTime = models.DateTimeField(verbose_name="Время порыва")
    windBearing = models.IntegerField(verbose_name="Направление ветра")

    cloudCover = models.FloatField("Облачность")
    uvIndex = models.IntegerField(verbose_name="УВ-индекс (time)")
    uvIndexTime = models.DateTimeField(verbose_name="УВ-индекс (value)")
    ozone = models.FloatField(verbose_name="Озон")

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = "Погода за день"
        verbose_name_plural = "Погода за дни"
        ordering = ["date", "city"]

    '''


class HourlyWeather(models.Model):
    response_datetime = models.DateTimeField(verbose_name="Дата и время запроса", auto_now_add=True)
    response_text = models.CharField(max_length=2000, verbose_name="Ответ сервера")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")

    date = models.DateTimeField(verbose_name="Дата")  # original name = time
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
        return self.city

    class Meta:
        verbose_name = "Погода за час"
        verbose_name_plural = "Почасовая погода"
        ordering = ["city"]
