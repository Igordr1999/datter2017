from django.db import models
from datetime import datetime


class Valuta(models.Model):
    name_ru = models.CharField(verbose_name="Название (RU)", max_length=100, unique=True)
    name_en = models.CharField(verbose_name="Название (EN)", max_length=100, unique=True)
    char_code = models.CharField(verbose_name="Символьный код", max_length=3, unique=True)
    num_code = models.CharField(verbose_name="Числовой код", max_length=3, unique=True)
    nominal = models.IntegerField(verbose_name="Номинал", default=1)
    description = models.TextField(verbose_name="Описание", max_length=300)
    icon = models.ImageField(verbose_name="Иконка", upload_to='currency/icon/')

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
        ordering = ["name_ru"]


class ValutaValue(models.Model):
    valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE, verbose_name="Валюта")
    date = models.DateField(verbose_name="Дата")
    DIRECTION_CHOICE = (
        ("T", 'Вверх'),
        ("D", 'Вниз'),
        ("N", 'Без изменений'),
    )
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
    # p = ValutaValue(valuta=Valuta.objects.first(), date=date(2016, 1, 2), value=55.6677)
    # p.save()

    # from datetime import datetime
    # epoch = datetime.utcfromtimestamp(0)
    # q = (d - epoch).total_seconds() * 1000
    # int(q)
    # 1515715200000

    class Meta:
        verbose_name = "Котировка валюты"
        verbose_name_plural = "Котировки валют"
        ordering = ["-date"]
        unique_together = ("valuta", "date")
