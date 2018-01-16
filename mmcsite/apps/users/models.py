# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your models here.
from django.db import models
import hashlib

TEXT_MAX_LEN = 64
DESCRIPTION_MAX_LEN = 512

class CompanyProfile(models.Model):
    """
    公司
    """
    id = models.AutoField(max_length=64, primary_key=True, verbose_name="")
    company = models.CharField(max_length=TEXT_MAX_LEN, blank=False,verbose_name=u"公司名称")
    street = models.CharField(max_length=TEXT_MAX_LEN, blank=True,verbose_name=u"公司街道")
    postal_code = models.CharField(max_length=TEXT_MAX_LEN, blank=True,verbose_name=u"邮政")
    city = models.CharField(max_length=DESCRIPTION_MAX_LEN, blank=True,verbose_name=u"城市")
    Image =  models.FileField(upload_to="image/%Y/%m",max_length=100,blank=True,verbose_name=u"图片")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __unicode__(self):
        return self.company


class User(models.Model):
    """
    用户表
    """
    TYPE_CHOICE = (
        (0, u"摄氏度"),
        (1, u"华氏度"),
    )
    username = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"用户名")
    password = models.CharField(max_length=64, null=True, blank=True, verbose_name=u"密码")
    email = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"邮箱")
    is_lock = models.BooleanField(default=0, verbose_name=u"是否锁定")
    temperature_unit = models.SmallIntegerField(choices=TYPE_CHOICE, null=True, blank=True, verbose_name="展示类型")
    note = models.CharField(max_length=512, null=True, blank=True, verbose_name=u"电话")
    role = models.ManyToManyField(to="Role", verbose_name=u"用户关联的角色")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
    iotprofile = models.ForeignKey(CompanyProfile, null=True, blank=True, verbose_name=u'公司')

    class Meta:
        verbose_name_plural = u"用户表"

    def __unicode__(self):
        return self.username

    # #自定义加密 重写save方法
    # def save(self, *args, **kwargs):
    #     self.password = hashlib.sha1(self.password + self.username).hexdigest()
    #     super(User, self).save(*args, **kwargs)


class Role(models.Model):
    """
    角色表
    """
    role = models.CharField(max_length=32, verbose_name=u"角色名称")
    is_show = models.BooleanField(default=0, verbose_name=u"是否展示")
    groups = models.ManyToManyField(to="PermissionsGroup", verbose_name=u"角色关联的权限组")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")

    class Meta:
        verbose_name_plural = u"角色表"

    def __unicode__(self):
        return self.role


class Permissions(models.Model):
    """
        权限表
    """
    name = models.CharField(max_length=32,null=True, blank=True, verbose_name=u"标题")
    url = models.CharField(max_length=128,null=True, blank=True, verbose_name=u"URL")
    code = models.CharField(max_length=16,null=True, blank=True, verbose_name=u"权限码")

    class Meta:
        verbose_name_plural = u"权限表"

    def __unicode__(self):
        return self.url


class PermissionsGroup(models.Model):
    """
        权限组表
    """
    name = models.CharField(max_length=32, null=True, verbose_name=u"权限组名")
    is_show = models.BooleanField(default=0, verbose_name=u"是否展示")
    permissions = models.ManyToManyField(to="Permissions", blank=True, verbose_name=u'权限表')

    class Meta:
        verbose_name_plural = u"权限组表"

    def __unicode__(self):
        return unicode(self.name)


class IotMedicine(models.Model):
    DEVICE_TYPE_CHOICES = (
        (1, 'iOS'),
        (2, 'Android'),
        (0, 'Common')
    )

    company = models.CharField(max_length=TEXT_MAX_LEN, blank=True)
    secret_key = models.CharField(max_length=TEXT_MAX_LEN, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    bundle_id = models.CharField(max_length=TEXT_MAX_LEN)
    package_name = models.CharField(max_length=TEXT_MAX_LEN)
    type = models.IntegerField(choices=DEVICE_TYPE_CHOICES, default=0)
    app_id = models.CharField(max_length=TEXT_MAX_LEN, blank=False)
    token = models.CharField(max_length=TEXT_MAX_LEN, default='0')
    description = models.CharField(max_length=DESCRIPTION_MAX_LEN, blank=True)
    # class Meta:
    # 	app_label = 'iot'

    def __unicode__(self):
        return unicode(self.id) + unicode(':') + unicode(self.type)


class Message(models.Model):
    """
    操作日志
    """
    login_time = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    username = models.CharField(max_length=32, null=True, blank=True, verbose_name=u"用户名")
    message = models.CharField(max_length=TEXT_MAX_LEN, default='0', verbose_name=u'操作信息')
    user = models.ForeignKey(to='User', blank=True, null=True, verbose_name=u"用户")

    def __unicode__(self):
        return self.message














