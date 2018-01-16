from django.db import models
from datetime import datetime

DIRECTION_CHOICE = (
        ("T", 'Вверх'),
        ("D", 'Вниз'),
        ("N", 'Без изменений'),
    )


class Valuta(models.Model):
    name_ru = models.CharField(verbose_name="Название (RU)", max_length=100, unique=True)
    name_en = models.CharField(verbose_name="Название (EN)", max_length=100, unique=True)
    char_code = models.CharField(verbose_name="Символьный код", max_length=3, unique=True)
    num_code = models.CharField(verbose_name="Числовой код", max_length=3, unique=True)
    nominal = models.IntegerField(verbose_name="Номинал", default=1)
    description = models.TextField(verbose_name="Описание", max_length=300)
    icon = models.ImageField(verbose_name="Иконка", upload_to='currency/icon/')
    popular = models.BooleanField(verbose_name="Популярная валюта", default=False)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
        ordering = ["name_ru"]


class ValutaValue(models.Model):
    valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE, verbose_name="Валюта")
    date = models.DateField(verbose_name="Дата")
    direction_change = models.CharField(max_length=1, choices=DIRECTION_CHOICE, default="N",
                                        verbose_name="Направление изменения курса")
    percent_change = models.FloatField(verbose_name="Процентное изменение курса", default=0.00)
    value = models.FloatField(verbose_name="Значение", default=60.1234)

    def save(self, *args, **kwargs):
        last_value = ValutaValue.objects.filter(valuta=self.valuta).first().value
        change_value = self.value - last_value
        self.percent_change = round(change_value/last_value*100, 2)
        if change_value > 0:
            self.direction_change = "T"
        elif change_value < 0:
            self.direction_change = "D"
        else:
            self.direction_change = "N"
        super(ValutaValue, self).save(*args, **kwargs)

    @staticmethod
    def add_value(valuta, day, month, year, value):
        my_date = datetime(day=day, month=month, year=year)
        my_valuta = Valuta.objects.get(char_code=valuta)
        ValutaValue.objects.create(valuta=my_valuta, date=my_date, value=value)

        # ValutaValue.add_value("USD", 2, 2, 2018, 65.2234)

    class Meta:
        verbose_name = "Котировка валюты"
        verbose_name_plural = "Котировки валют"
        ordering = ["-date"]
        unique_together = ("valuta", "date")
