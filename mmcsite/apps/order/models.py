# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.

from django.db import models

from express.models import IotExpress
from users.models import User
from device.models import IotDevice

TEXT_LEN = 32
TEXT_MAX_LEN = 64
DESCRIPTION_MAX_LEN = 128

STATUS_INIT = 1
STATUS_DONE = 2
STATUS_ALL = STATUS_INIT | STATUS_DONE

NOT_VALID_TEMPERATURE = -200


# how to save the update information(who made the update, what field is updated)
class IotOrder(models.Model):
    mac = models.CharField(max_length=TEXT_LEN, blank=True)
    number = models.CharField(max_length=TEXT_MAX_LEN, blank=True)
    device = models.ForeignKey(IotDevice, related_name='device_orders', blank=True, null=True)
    express = models.ForeignKey(IotExpress, related_name='express_orders', blank=True, null=True)
    owner = models.ForeignKey(User, related_name='user_orders', blank=True,
                              null=True)  # people who register the order is the owner
    start_time = models.DateTimeField(auto_now=False)
    end_time = models.DateTimeField(auto_now=False, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    high_temp = models.FloatField(default=40.0)
    low_temp = models.FloatField(default=0.0)
    highest_temp = models.FloatField(
        default=NOT_VALID_TEMPERATURE)  # for quickly identify temperature exception in web, server count the value
    lowest_temp = models.FloatField(default=NOT_VALID_TEMPERATURE)  # for quickly identify temperature exception in web
    status = models.IntegerField(default=STATUS_INIT)
    description = models.CharField(max_length=DESCRIPTION_MAX_LEN, blank=True)
    extra_data = models.CharField(max_length=TEXT_LEN, blank=True)
    coordinate = models.CharField(max_length=TEXT_LEN, blank=True)

    class Meta:
        app_label = 'iot'


class IotMedicineOrder(models.Model):
    mac = models.CharField(max_length=TEXT_LEN, blank=True)
    number = models.CharField(max_length=TEXT_MAX_LEN, blank=True)
    # device = models.ForeignKey('IotDevice', related_name='IotDevice', blank=True, null=True)
    # express = models.ForeignKey('IotExpress', related_name='IotExpress', blank=True, null=True)
    # owner = models.ForeignKey('IotUser', related_name='IotUser', blank=True, null=True) #people who register the order is the owner
    start_time = models.DateTimeField(auto_now=False)
    end_time = models.DateTimeField(auto_now=False, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    high_temp = models.FloatField(default=40.0)
    low_temp = models.FloatField(default=0.0)
    highest_temp = models.FloatField(
        default=NOT_VALID_TEMPERATURE)  # for quickly identify temperature exception in web, server count the value
    lowest_temp = models.FloatField(default=NOT_VALID_TEMPERATURE)  # for quickly identify temperature exception in web
    status = models.IntegerField(default=STATUS_INIT)
    description = models.CharField(max_length=DESCRIPTION_MAX_LEN, blank=True)
    extra_data = models.CharField(max_length=TEXT_LEN, blank=True)
    coordinate = models.CharField(max_length=TEXT_LEN, blank=True)

    class Meta:
        # db_table = 'IotOrder'
        app_label = 'iot'

