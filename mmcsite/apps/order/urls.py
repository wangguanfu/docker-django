# from django.conf.urls import patterns, url
import views  as order
from django.conf.urls import url

urlpatterns = [
    # urls for device
    url(r'^register/', order.register),
    url(r'^update/', order.update),
    url(r'^get/', order.get),
    url(r'^time/', order.time),
    url(r'^in_delivery/', order.in_delivery),
    url(r'^created_today', order.created_today),
    url(r'^delivered_today', order.delivered_today),
]
