# from django.conf.urls import patterns, url
import views as temperature
from django.conf.urls import url

urlpatterns = [
    # urls for device
    url(r'^post/', temperature.post),
    url(r'^get/', temperature.get),
    url(r'^get_seq/', temperature.get_seq),
    url(r'^get_compressed/', temperature.get_compressed),
    url(r'^delete/', temperature.delete),
]
