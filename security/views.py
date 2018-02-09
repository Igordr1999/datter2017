from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Profile
from .forms import UserForm, ProfileForm, EditPassword
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


@login_required
@transaction.atomic
def update_profile(request):
    alert = ""
    template = 'security/upgrade_profile.html'
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            # Моя валидация username, first and last name. Если все ок, то сохранение.
            alert = Profile.check_user_update(user_form, profile_form)
        else:
            alert = "Данные некорректны"
        return render(request, template, {
            'user_form': user_form,
            'profile_form': profile_form,
            'alert_primary': alert
        })
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, template, {
            'user_form': user_form,
            'profile_form': profile_form
        })


@login_required
def update_password(request):
    alert = ""
    if request.method == 'POST':
        edit_password_form = EditPassword(request.POST)
        if edit_password_form.is_valid():
            my_username = request.user.username
            now_password = edit_password_form.cleaned_data["now_password"]
            new_password = edit_password_form.cleaned_data["new_password"]
            repeat_new_password = edit_password_form.cleaned_data["repeat_new_password"]

            if not request.user.check_password(raw_password=now_password):
                alert = "Текущий пароль неправильный"
            elif new_password != repeat_new_password:
                alert = "Новые пароли НЕ совпадают"
            else:
                # меняем пароль
                u = User.objects.get(username=my_username)
                u.set_password(new_password)
                u.save()

                alert = "Пароль обновлен"
        else:
            alert = "Данные некорректны"
    else:
        edit_password_form = EditPassword()
    return render(request, 'security/upgrade_password.html', {
        'password_form': edit_password_form,
        'alert_primary': alert
    })


def login_profile(request):
    if request.user.is_authenticated:
        return redirect('/')

    alert = ""
    template = 'security/login.html'
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            alert = "Логин и пароль неправильные"
        return render(request, template, {'alert_danger': alert})
    return render(request, template)


def logout_profile(request):
    logout(request)
    return redirect('/')
