# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.
from django.db import models
from users.models import User

TEXT_MAX_LEN = 64
EXTENSION_MAX_LEN = 128
LARGE_TEXT_MAX_LEN = 1028

PAY_QUERY_OK = 1
PAY_QUERY_FAIL = 0

class IotExpress_Kuaidiwang(models.Model):
    express_company_name = models.CharField(max_length=TEXT_MAX_LEN, blank=False, unique=True)
    company_code = models.CharField(max_length=TEXT_MAX_LEN, blank=False, unique=True)
    description = models.CharField(max_length=EXTENSION_MAX_LEN,blank=True)

    class Meta:
        app_label = 'iot'
# Create your models here.

#class IotExpressCompany(models.Model):

class vendorcompany(models.Model):
    EXPRESS_TYPE_CHOICES = (
        ('W', 'Kuaidiwang'),
        ('F', 'Kuaidi100'),
    )
    vendor = models.CharField(max_length=1, choices=EXPRESS_TYPE_CHOICES, default='W')
    company_name = models.CharField(max_length=TEXT_MAX_LEN, blank=True, null=True)
    company_code = models.CharField(max_length=TEXT_MAX_LEN)
    icon = models.CharField(max_length=LARGE_TEXT_MAX_LEN, blank=True, null=True)

    class Meta:
        # db_table = 'IotTemp'
        app_label = 'iot'
        unique_together = (("vendor", "company_code"),)


class IotExpress(models.Model):
    number =  models.CharField(max_length=TEXT_MAX_LEN, blank=False)
    company = models.ForeignKey(vendorcompany, related_name='express_company', blank=True, null=True)
    status = models.IntegerField(default=0)
    data = models.TextField(blank=True, null=True)
    desResult = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    pay_status=models.IntegerField(default=0)
    description = models.CharField(max_length=EXTENSION_MAX_LEN,blank=True, null=True)

    class Meta:
        #db_table = 'IotExpress'
        app_label = 'iot'

    def __unicode__(self):
        return unicode(self.id) + unicode(':') + unicode(self.number)
