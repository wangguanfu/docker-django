"""mmcsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
import users.urls
import event.urls
import express.urls
import order.urls
import temperature.urls
import device.urls
# import log.urls
#

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include(users.urls, namespace="users")),
    # url(r'^users/', include(users.urls, namespace="users")),
    url(r'^event/', include(event.urls, namespace="event")),
    url(r'^express/', include(express.urls, namespace="express")),
    url(r'^order/', include(order.urls, namespace="order")),
    url(r'^temperature/', include(temperature.urls, namespace="temperature")),
    url(r'^device/', include(device.urls, namespace="device")),
    # url(r'^log/', include(log.urls, namespace="log")),
]
