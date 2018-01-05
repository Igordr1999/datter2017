from django.db import models


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
    value = models.FloatField(verbose_name="Значение", default=10.0000)

    # p = ValutaValue(valuta=Valuta.objects.first(), date=date(2016, 1, 2), value=55.6677)
    # p.save()

    class Meta:
        verbose_name = "Котировка валюты"
        verbose_name_plural = "Котировки валют"
        ordering = ["date"]
        unique_together = ("valuta", "date")
