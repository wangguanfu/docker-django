# from django.conf.urls import patterns, url
import views as event
from django.conf.urls import url

urlpatterns = [
    # urls for device
    url(r'^post/', event.device_update_event_post),
]
