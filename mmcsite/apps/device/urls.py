# from django.conf.urls import patterns, url
import views as device
from django.conf.urls import url

urlpatterns = [
    # urls for device
    url(r'^register/', device.register),
    url(r'^update/', device.update),
    url(r'^get/', device.get),
    url(r'^get_device/', device.get_device),
    url(r'^add_device/', device.add_device),
    url(r'^edit_device/', device.edit_device),
    url(r'^search/', device.search),
    url(r'^edit_profile/', device.edit_profile),
    url(r'^add_profile/', device.add_profile),
]
