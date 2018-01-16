import  views as express
from django.conf.urls import url

urlpatterns = [
    # urls for device
    url(r'^register/', express.register),
    url(r'^get_latest/', express.get_latest),
    url(r'^get_count_bymonth/', express.get_count_bymonth)
    #url(r'^get/$', 'get', name='get'),
]
