from django.db import models
from currency.models import Valuta

aircraft_status_choice = (
    ("A", 'Active'),
    ("S", 'Stored'),
    ("W", 'Written Off'),
    ("U", 'Scrapped'),
    ("C", 'Crashed'),
    ("O", 'On Order'),
)


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


class Alliance(models.Model):
    name_en = models.CharField(verbose_name="Название EN", max_length=200, unique=True)
    logo = models.ImageField(verbose_name="Лого", upload_to='data/alliance/logo/', default='data/alliance/logo/no.jpg')

    def __str__(self):
        return self.name_en

    class Meta:
        verbose_name = "Альянс"
        verbose_name_plural = "Альянсы"
        ordering = ["name_en"]


class Airport(models.Model):
    name_ru = models.CharField(verbose_name="Название RU", max_length=200, unique=True)
    name_en = models.CharField(verbose_name="Название EN", max_length=200, unique=True)
    iata_code = models.CharField(verbose_name="IATA код", max_length=3, unique=True)
    icao_code = models.CharField(verbose_name="ICAO код", max_length=4, unique=True)
    latitude = models.FloatField(verbose_name="Широта", unique=True)
    longitude = models.FloatField(verbose_name="Долгота", unique=True)
    altitude = models.IntegerField(verbose_name="Высота")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")
    logo = models.ImageField(verbose_name="Лого", upload_to='data/airport/logo/', default='data/airport/logo/no.jpg')

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Аэропорт"
        verbose_name_plural = "Аэропорты"
        ordering = ["name_ru"]


class Airline(models.Model):
    name_ru = models.CharField(verbose_name="Название RU", max_length=200, unique=True)
    name_en = models.CharField(verbose_name="Название EN", max_length=200, unique=True)
    iata_code = models.CharField(verbose_name="IATA код", max_length=2, unique=True)
    icao_code = models.CharField(verbose_name="ICAO код", max_length=3, unique=True)
    logo = models.ImageField(verbose_name="Лого", upload_to='data/airline/logo/', default='data/airline/logo/no.jpg')
    alliance = models.ForeignKey(Alliance, on_delete=models.CASCADE, verbose_name="Альянс", null=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Авиакомпания"
        verbose_name_plural = "Авиакомпании"
        ordering = ["name_ru"]


class AircraftType(models.Model):
    model_ru = models.CharField(verbose_name="Название RU", max_length=200, unique=True)
    model_en = models.CharField(verbose_name="Название EN", max_length=200, unique=True)
    icao_code = models.CharField(verbose_name="Код ICAO", max_length=4, unique=True)
    iata_code = models.CharField(verbose_name="Код IATA", max_length=3, default="N/A")

    def __str__(self):
        return self.model_ru

    class Meta:
        verbose_name = "Тип самолета"
        verbose_name_plural = "Типы самолетов"
        ordering = ["model_ru"]


class Aircraft(models.Model):
    model = models.ForeignKey(AircraftType, on_delete=models.CASCADE, verbose_name="Модель")
    modification = models.CharField(verbose_name="Модификация", max_length=100)
    msn = models.IntegerField(verbose_name="MSN")
    registration = models.CharField(verbose_name="Код самолета", max_length=10, unique=True)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, verbose_name="Владелец")
    create_date = models.DateField(verbose_name="Создан")
    status = models.CharField(max_length=1, choices=aircraft_status_choice, default="A",
                              verbose_name="Состояние")
    note = models.TextField(verbose_name="Примечания", max_length=500)
    logo = models.ImageField(verbose_name="Фото в данной ливрее", upload_to='data/aircraft/example/',
                             default='data/aircraft/example/no.jpg')

    def __str__(self):
        return self.registration

    class Meta:
        verbose_name = "Самолет"
        verbose_name_plural = "Самолеты"
        ordering = ["registration"]
