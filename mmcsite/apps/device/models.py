# -*- coding: utf-8 -*-
from django.db import models
from users.models import User
# from django.utils import timezone


TEXT_MAX_LEN = 32
DESCRIPTION_MAX_LEN = 521


class IotDevice(models.Model):
    device_id = models.AutoField(primary_key=True)
    mac_addr = models.CharField(max_length=TEXT_MAX_LEN, blank=False, unique=True)
    serial_num = models.CharField(max_length=TEXT_MAX_LEN, blank=True)
    model_num = models.CharField(max_length=TEXT_MAX_LEN, blank=True)
    firmware_rev = models.CharField(max_length=TEXT_MAX_LEN, blank=True)
    software_rev = models.CharField(max_length=TEXT_MAX_LEN, blank=True)
    hardware_rev = models.CharField(max_length=TEXT_MAX_LEN, blank=True)
    #battery_level = models.IntegerField(default=100) //move to event
    time_registered = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    # class Meta:
    #     app_label = 'iot'

    def __unicode__(self):
        return unicode(self.device_id) + unicode(':') + unicode(self.mac_addr) + unicode('-') + unicode(self.serial_num)

#
#
# class Profile(models.Model):
#     """
#     设备描述
#     """
#     id = models.AutoField(max_length=64, primary_key=True, verbose_name="")
#     name = models.CharField(max_length=TEXT_MAX_LEN, blank=False)
#     device_field = models.CharField(max_length=TEXT_MAX_LEN, verbose_name=u'设备类型')
#     description = models.CharField(max_length=DESCRIPTION_MAX_LEN, blank=True)
#     high_temperature = models.CharField(max_length=TEXT_MAX_LEN, verbose_name=u'最高温度')
#     low_temperature = models.CharField(max_length=TEXT_MAX_LEN, verbose_name=u'最低温度')
#     delayed = models.IntegerField(blank=True, null=True, verbose_name=u'延时开始')
#     record_interval = models.IntegerField(blank=True, null=True, verbose_name=u'记录间隔')
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
#
#     def __unicode__(self):
#         return self.name
#

class DeviceProfile(models.Model):
    """
    设备设置
    """

    name = models.CharField(max_length=TEXT_MAX_LEN, verbose_name=u"设备名")
    type_choices = ((1, u'mac'),
                    (2, u'Common'),
                    (3, u'android'),)
    type = models.IntegerField(choices=type_choices, null=True, blank=True, verbose_name=u'设备类型')
    describe = models.TextField(max_length=DESCRIPTION_MAX_LEN, null=True, blank=True, verbose_name=u'描述')
    high_temperature = models.CharField(max_length=TEXT_MAX_LEN, null=True, blank=True, verbose_name=u'最高温度')
    low_temperature = models.CharField(max_length=TEXT_MAX_LEN, null=True, blank=True, verbose_name=u'最低温度')
    delayed = models.IntegerField(blank=True, null=True, verbose_name=u'延时开始')
    record_interval = models.IntegerField(blank=True, null=True, verbose_name=u'记录间隔')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")

    def __unicode__(self):
        return self.name


class Device(models.Model):
    """
    设备表
    """
    SN = models.CharField(max_length=TEXT_MAX_LEN)
    users = models.ManyToManyField(to=User, verbose_name=u'所属用户')

    state_choices = ((1, u'正常'),
                     (2, u'异常'),)
    state = models.IntegerField(choices=state_choices, default=1, verbose_name=u'状态')
    model_choices = ((1, u'活跃'),
                     (2, u'存档'))
    model = models.IntegerField(choices=model_choices, default=1, verbose_name=u'激活状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    profile = models.OneToOneField(to=DeviceProfile, null=True, blank=True, verbose_name=u"设备描述")

    def __unicode__(self):
        return unicode(self.SN)


class CustomFields(models.Model):
    """
    自定义字段
    """
    content = models.CharField(max_length=DESCRIPTION_MAX_LEN, verbose_name=u"字段内容")
    type_choices = ((1, u"text"), (2, u"integer"))
    type = models.IntegerField(choices=type_choices, verbose_name=u"字段类型")
    device = models.OneToOneField(to=Device, null=True, blank=True, verbose_name=u"自定义字段")
















