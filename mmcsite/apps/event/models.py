# coding:utf8
from __future__ import unicode_literals
from django.db import models
from order.models import IotOrder
from users.models import User
from device.models import IotDevice

TEXT_MAX_LEN = 64
EXTENSION_MAX_LEN = 128
LARGE_TEXT_MAX_LEN = 1028


# event for order, register, update
class IotOrderEvent(models.Model):
	#company_id = models.ForeignKey(IotExpress_Kuaidiwang, related_name='company_id')
    EVENT_TYPE_CHOICES = (
        (1, 'Register'),
        (2, 'Update start time'),
        (3, 'Update end time'),
        (0, "No event"),
    )
    order = models.ForeignKey(IotOrder, related_name='order_events')
    user = models.ForeignKey(User, related_name='user_events', blank=True, null=True)
    type = models.IntegerField(choices=EVENT_TYPE_CHOICES, default=2)
    time = models.DateTimeField(auto_now_add=True)
    extra = models.CharField(max_length=TEXT_MAX_LEN, blank=True)
    description = models.CharField(max_length=EXTENSION_MAX_LEN,blank=True)

    class Meta:
        app_label = 'iot'

    def __unicode__(self):
        return unicode(self.id) + unicode(':') + unicode(self.type)


class IotDeviceEvent(models.Model):
	#company_id = models.ForeignKey(IotExpress_Kuaidiwang, related_name='company_id')
    EVENT_TYPE_CHOICES = (
        (1, 'battery'),
        (0, "No event"),
    )
    device = models.ForeignKey(IotDevice, related_name='device_events')
    type = models.IntegerField(choices=EVENT_TYPE_CHOICES, default=1)
    time = models.DateTimeField(auto_now_add=True)
    extra = models.CharField(max_length=TEXT_MAX_LEN, blank=True)
    description = models.CharField(max_length=EXTENSION_MAX_LEN,blank=True)

    class Meta:
        app_label = 'iot'

    def __unicode__(self):
        return unicode(self.id) + unicode(':') + unicode(self.type)