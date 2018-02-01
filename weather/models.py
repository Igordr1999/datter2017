from django.db import models
from data.models import City


class HourlyForecastWeather(models.Model):
    raw_response_datetime = models.DateTimeField(verbose_name="Дата и время запроса", auto_now_add=True)
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
        return str(str(self.city) + " " + str(self.datetime_utc))

    class Meta:
        verbose_name = "Погода за час"
        verbose_name_plural = "Почасовая погода"
        ordering = ["city", "datetime_utc"]


class DailyForecastWeather(models.Model):
    raw_response_datetime = models.DateTimeField(verbose_name="Дата и время запроса", auto_now_add=True)
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

    temperatureMax = models.FloatField(verbose_name="Наибольшая температура")
    temperatureMin = models.FloatField(verbose_name="Наименьшая температура")
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

    # situation_XX - Ситуация на XX часов по местному времени (ссылка на этот час по UTC)
    situation_0 = models.ForeignKey(HourlyForecastWeather, on_delete=models.CASCADE,
                                   related_name="zero_hours", verbose_name="Прогноз на 0 часов")
    situation_3 = models.ForeignKey(HourlyForecastWeather, on_delete=models.CASCADE,
                                    related_name="three_hours", verbose_name="Прогноз на 3 часов")
    situation_6 = models.ForeignKey(HourlyForecastWeather, on_delete=models.CASCADE,
                                  related_name="six_hours", verbose_name="Прогноз на 6 часов")
    situation_9 = models.ForeignKey(HourlyForecastWeather, on_delete=models.CASCADE,
                                   related_name="nine_hours", verbose_name="Прогноз на 9 часов")
    situation_12 = models.ForeignKey(HourlyForecastWeather, on_delete=models.CASCADE,
                                     related_name="twelve_hours", verbose_name="Прогноз на 12 часов")
    situation_15 = models.ForeignKey(HourlyForecastWeather, on_delete=models.CASCADE,
                                      related_name="fifteen_hours", verbose_name="Прогноз на 15 часов")
    situation_18 = models.ForeignKey(HourlyForecastWeather, on_delete=models.CASCADE,
                                       related_name="eighteen_hours", verbose_name="Прогноз на 18 часов")
    situation_21 = models.ForeignKey(HourlyForecastWeather, on_delete=models.CASCADE,
                                         related_name="twenty_one_hours", verbose_name="Прогноз на 21 часов")

    def __str__(self):
        return str(str(self.city) + " " + str(self.datetime_utc))

    class Meta:
        verbose_name = "Погода на день"
        verbose_name_plural = "Погода на дни"
        ordering = ["city", "datetime_utc"]

