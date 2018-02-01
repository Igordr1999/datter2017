"""datter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from home import views as home_views
from currency import views as currency_views
from data import views as data_views
from weather import views as weather_views
from django.conf.urls import include

urlpatterns = [
    # Системные
    path('froala_editor/', include('froala_editor.urls')),
    path('admin/', admin.site.urls),

    # Приложение home
    path('', home_views.home, name="home"),
    path('blog/', home_views.blog, name="blog"),
    path('blog/article/<int:num>/', home_views.blog_article, name="blog_article"),
    path('blog/section/<int:num>/', home_views.blog_section, name="blog_section"),
    path('blog/sections/', home_views.blog_sections, name="blog_sections"),
    path('terms/', home_views.terms, name="terms"),
    path('personal_data_policy/', home_views.personal_data_policy, name="personal_data_policy"),

    # Приложение currency
    path('currency/', currency_views.currency_home, name="currency"),
    path('currency/converter/', currency_views.currency_converter, name="currency_converter"),
    path('currency/<code>/', currency_views.currency_values, name="currency_values"),
    path('currency/<code>/info/', currency_views.currency_valuta_info, name="currency_valuta_info"),

    # Приложение data. Раздел - data
    path('time/', data_views.time_home, name="time_home"),
    path('time/cities/', data_views.time_cities, name="time_cities"),
    path('time/timezones/', data_views.time_timezones, name="time_timezones"),
    path('time/<name>/', data_views.time_city, name="time_city"),
    path('time/zone/<path:name>/', data_views.time_timezone, name="time_timezone"),

    # Приложение data. Раздел - weather
    path('weather/<name>/', weather_views.forecast_7days, name="forecast_7days"),
    path('weather/<name>/<int:day>/<int:month>/<int:year>/', weather_views.forecast_for_day, name="forecast_for_day"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
