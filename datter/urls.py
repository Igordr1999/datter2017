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
from home import views
from django.conf.urls import include

urlpatterns = [
    path('froala_editor/', include('froala_editor.urls')),
    path('page/', views.page, name="page"),
    path('admin/', admin.site.urls),
    # home
    path('', views.home, name="home"),
    path('blog/', views.blog, name="blog"),
    path('blog/article/<int:num>/', views.blog_article, name="blog_article"),
    path('terms/', views.terms, name="terms"),
    path('personal_data_policy/', views.personal_data_policy, name="personal_data_policy"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
