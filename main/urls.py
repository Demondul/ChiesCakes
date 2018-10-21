"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('apps.Home.urls')),
    url(r'^flavors/', include('apps.Flavors.urls', 'flavors'), name='flavors'),
    url(r'^gallery/', include('apps.Gallery.urls', 'gallery'), name='gallery'),
    url(r'^info/', include('apps.Info.urls', 'info'), name='info'),
    url(r'^profile/', include('apps.Profile.urls', 'profile'), name='profile'),
    url(r'^reservations/', include('apps.Reservations.urls', 'reservations'), name='reservations'),
    url(r'^reviews/', include('apps.Reviews.urls', 'reviews'), name='reviews')
]
