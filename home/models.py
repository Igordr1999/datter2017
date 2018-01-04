from django.db import models
from django.contrib.auth.models import User


class Section(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание", max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ["name"]


class BlogArticle(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name="Раздел")
    time_publication = models.DateTimeField(verbose_name="Время публикации", auto_now_add=True)
    time_last_update = models.DateTimeField(verbose_name="Последнее обновление", auto_now=True)
    preview_text = models.CharField(verbose_name="Короткое описание", max_length=500)
    text = models.TextField(verbose_name="Текст", max_length=4000)
    preview_photo = models.ImageField(verbose_name="Предварительное фото", upload_to='blog/preview_photo/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-time_publication"]
