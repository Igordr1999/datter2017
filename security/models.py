from django.db import models
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.validators import ASCIIUsernameValidator
import re

from data.models import City

sex_choice = (
    ("M", 'Мужчина'),
    ("W", 'Женщина'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    sex = models.CharField(max_length=1, choices=sex_choice, default="N", verbose_name="Пол")
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    location = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Основной город")
    birth_date = models.DateField(verbose_name="Дата рождения")

    @staticmethod
    def check_user_update(user_form, profile_form):
        fn = user_form.cleaned_data["first_name"]
        ln = user_form.cleaned_data["last_name"]
        un = user_form.cleaned_data["username"]
        tpl = '^[a-zA-Z][a-zA-Z0-9_]{3,19}$'
        if len(fn) < 2 or len(fn) > 30 or len(ln) < 2 or len(ln) > 30:
            alert = "Имя или Фамилия не состоят из 2-30 символов!"
        elif re.match(tpl, un) is not None:
            user_form.save()
            profile_form.save()
            alert = "Настройки обновлены"
        else:
            alert = 'UserName может состоять только из латинских букв, цифр и "_". Длина 4-20 символов.' \
                    'Первым символом должна быть БУКВА!'
        return alert


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ["user"]
