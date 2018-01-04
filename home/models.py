from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField


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
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name="Раздел")
    time_publication = models.DateTimeField(verbose_name="Время публикации", auto_now_add=True)
    time_last_update = models.DateTimeField(verbose_name="Последнее обновление", auto_now=True)
    preview_text = models.CharField(verbose_name="Короткое описание", max_length=500)
    content = FroalaField(verbose_name="Контент", default="NO CONTENT")
    preview_photo = models.ImageField(verbose_name="Предварительное фото", upload_to='blog/preview_photo/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["time_publication"]


class Page(models.Model):
    content = FroalaField()
