from __future__ import unicode_literals

from django.db import models
from order.models import IotOrder
from device.models import IotDevice

DESCRIPTION_MAX_LEN = 128

# Create your models here.
class IotTemp(models.Model):
	mac = models.CharField(max_length=64, blank=False)
	device = models.ForeignKey(IotDevice,blank=True, null=True)
	temperature = models.FloatField(default=0.0)
	seq_no = models.IntegerField()
	time = models.DateTimeField(auto_now=False)
	description = models.CharField(max_length=DESCRIPTION_MAX_LEN,blank=True)

	class Meta:
		#db_table = 'IotTemp'
		app_label='iot'
		unique_together = (("mac", "seq_no"),)

class IotMedicineTemp(models.Model):
	mac = models.CharField(max_length=64, blank=False)
	device = models.ForeignKey('IotDevice',related_name='IotDevice',blank=True, null=True)
	temperature = models.FloatField(default=0.0)
	seq_no = models.IntegerField()
	time = models.DateTimeField(auto_now=False)
	description = models.CharField(max_length=DESCRIPTION_MAX_LEN,blank=True)

	class Meta:
		#db_table = 'IotTemp'
		app_label='iot'
		unique_together = (("mac", "seq_no"),)


