from django import forms
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


class EditPassword(forms.Form):
    now_password = forms.CharField(label="Текущий пароль", widget=forms.PasswordInput)
    new_password = forms.CharField(label="Придумайте новый пароль", widget=forms.PasswordInput)
    repeat_new_password = forms.CharField(label="Повторите новый пароль", widget=forms.PasswordInput)