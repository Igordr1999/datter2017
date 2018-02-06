from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('sex', 'bio', 'location', 'birth_date')

class RegForm(forms.ModelForm):
    pass