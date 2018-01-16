# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import DeviceProfile,IotDevice,Device
# Register your models here.


admin.site.register(DeviceProfile)
admin.site.register(IotDevice)
admin.site.register(Device)