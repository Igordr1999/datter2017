from django.db import models
from currency.models import Valuta


class Language(models.Model):
    name_ru = models.CharField(verbose_name="Название", max_length=50, unique=True)
    name_en = models.CharField(verbose_name="Международное название", max_length=50, unique=True)
    alpha2 = models.CharField(verbose_name="2-символьный код", max_length=2, unique=True)
    alpha3 = models.CharField(verbose_name="3-символьный код", max_length=3, unique=True)
    numeric = models.IntegerField(verbose_name="Числовой код", unique=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"
        ordering = ["name_ru"]


class TimeZone(models.Model):
    timeZoneId = models.CharField(verbose_name="Индификатор часового пояса", max_length=100, unique=True)
    timeZoneName = models.CharField(verbose_name="Полное название часового пояса", max_length=100, unique=True)
    rawOffset = models.IntegerField(verbose_name="Смещение от UTC (в секундах) для данного местоположения")
    dstOffset = models.IntegerField(verbose_name="Смещение для перехода на летнее время, выраженное в секундах",
                                    default=0)
    is_primary = models.BooleanField(verbose_name="Основное (предпочтительное) имя зоны")
    is_difference_dst = models.BooleanField(verbose_name="Смещение летом (АВТО)", default=False)
    utcRawOffset = models.CharField(verbose_name="Смещение от UTC (АВТО)", default="UTC", max_length=10)
    utcDstOffset = models.CharField(verbose_name="Смещение от UTC летом (АВТО)", default="UTC", max_length=10)

    def save(self, *args, **kwargs):
        # записывает отступы от UTC в часах в raw и dst. Если dst == 0, то нет летнего времени (is_difference_dst)
        raw = self.rawOffset / 3600
        if self.dstOffset == 0:
            self.is_difference_dst = False
            dst = 0
        else:
            self.is_difference_dst = True
            dst = self.dstOffset / 3600

        # записываем основной отступ. Например - UTC+3
        if raw >= 0:
            self.utcRawOffset = "UTC+{}".format(int(raw))
        else:
            self.utcRawOffset = "UTC{}".format(int(raw))

        # записываем летний отступ. Например - UTC+4
        dst_utc = int(raw+dst)
        if dst_utc >= 0:
            self.utcDstOffset = "UTC+{}".format(dst_utc)
        else:
            self.utcDstOffset = "UTC{}".format(dst_utc)

        super(TimeZone, self).save(*args, **kwargs)

    def __str__(self):
        return self.timeZoneName

    class Meta:
        verbose_name = "Часовой пояс"
        verbose_name_plural = "Часовые поясы"
        ordering = ["timeZoneName"]


class Region(models.Model):
    name_ru = models.CharField(verbose_name="Название", max_length=50, unique=True)
    name_en = models.CharField(verbose_name="Международное название", max_length=50, unique=True)
    alpha2 = models.CharField(verbose_name="2-символьный код", max_length=2, unique=True)
    numeric = models.IntegerField(verbose_name="Числовой код", unique=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
        ordering = ["name_ru"]


class SubRegion(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Регион")
    name_ru = models.CharField(verbose_name="Название", max_length=50, unique=True)
    name_en = models.CharField(verbose_name="Международное название", max_length=50, unique=True)
    alpha2 = models.CharField(verbose_name="2-символьный код", max_length=2, unique=True)
    numeric = models.IntegerField(verbose_name="Числовой код", unique=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Подрегион"
        verbose_name_plural = "Подрегионы"
        ordering = ["name_ru"]


class Country(models.Model):
    name_ru = models.CharField(verbose_name="Название", max_length=50, unique=True)
    name_en = models.CharField(verbose_name="Международное название", max_length=50, unique=True)
    full_name_ru = models.CharField(verbose_name="Полное название", max_length=100, unique=True)
    full_name_en = models.CharField(verbose_name="Полное международное название", max_length=100, unique=True)
    alpha2 = models.CharField(verbose_name="2-символьный код", max_length=2, unique=True)
    alpha3 = models.CharField(verbose_name="3-символьный код", max_length=3, unique=True)
    numeric = models.IntegerField(verbose_name="Числовой код", unique=True)
    area = models.IntegerField(verbose_name="Площадь в кв.км")
    population = models.IntegerField(verbose_name="Население")
    flag = models.ImageField(verbose_name="Флаг", upload_to='data/country/flag/',
                             default='data/country/flag/no_flag.jpg')
    coat_of_arms = models.ImageField(verbose_name="Герб", upload_to='data/country/coat_of_arms/',
                                     default='data/country/coat_of_arms/no_flag.jpg')
    sub_region = models.ForeignKey(SubRegion, on_delete=models.CASCADE, verbose_name="Подрегион")
    currency = models.ForeignKey(Valuta, on_delete=models.CASCADE, verbose_name="Основная валюта")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="Основной язык")

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ["name_ru"]


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна")
    name_ru = models.CharField(verbose_name="Название", max_length=50, unique=True)
    name_en = models.CharField(verbose_name="Международное название", max_length=50, unique=True)
    alpha3 = models.CharField(verbose_name="3-символьный код", max_length=3, unique=True)
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    is_capital = models.BooleanField(verbose_name="Столица", default=False)
    area = models.IntegerField(verbose_name="Площадь в кв.км")
    population = models.IntegerField(verbose_name="Население")
    flag = models.ImageField(verbose_name="Флаг", upload_to='data/city/flag/', default='data/city/flag/no_flag.jpg')
    coat_of_arms = models.ImageField(verbose_name="Герб", upload_to='data/city/coat_of_arms/',
                                     default='data/city/coat_of_arms/no_flag.jpg')
    time_zone = models.ForeignKey(TimeZone, on_delete=models.CASCADE, verbose_name="Часовой пояс")

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ["name_ru"]
