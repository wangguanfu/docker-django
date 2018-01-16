# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFields',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=521, verbose_name='\u5b57\u6bb5\u5185\u5bb9')),
                ('type', models.IntegerField(verbose_name='\u5b57\u6bb5\u7c7b\u578b', choices=[(1, 'text'), (2, 'integer')])),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('SN', models.CharField(max_length=32)),
                ('state', models.IntegerField(default=1, verbose_name='\u72b6\u6001', choices=[(1, '\u6b63\u5e38'), (2, '\u5f02\u5e38')])),
                ('model', models.IntegerField(default=1, verbose_name='\u6fc0\u6d3b\u72b6\u6001', choices=[(1, '\u6d3b\u8dc3'), (2, '\u5b58\u6863')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u8bbe\u5907\u540d')),
                ('type', models.IntegerField(blank=True, null=True, verbose_name='\u8bbe\u5907\u7c7b\u578b', choices=[(1, 'mac'), (2, 'pc'), (3, 'android')])),
                ('describe', models.TextField(max_length=521, null=True, verbose_name='\u63cf\u8ff0', blank=True)),
                ('high_temperature', models.CharField(max_length=32, null=True, verbose_name='\u6700\u9ad8\u6e29\u5ea6', blank=True)),
                ('low_temperature', models.CharField(max_length=32, null=True, verbose_name='\u6700\u4f4e\u6e29\u5ea6', blank=True)),
                ('delayed', models.IntegerField(null=True, verbose_name='\u5ef6\u65f6\u5f00\u59cb', blank=True)),
                ('record_interval', models.IntegerField(null=True, verbose_name='\u8bb0\u5f55\u95f4\u9694', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='IotDevice',
            fields=[
                ('device_id', models.AutoField(serialize=False, primary_key=True)),
                ('mac_addr', models.CharField(unique=True, max_length=32)),
                ('serial_num', models.CharField(max_length=32, blank=True)),
                ('model_num', models.CharField(max_length=32, blank=True)),
                ('firmware_rev', models.CharField(max_length=32, blank=True)),
                ('software_rev', models.CharField(max_length=32, blank=True)),
                ('hardware_rev', models.CharField(max_length=32, blank=True)),
                ('time_registered', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='profile',
            field=models.OneToOneField(null=True, blank=True, to='device.DeviceProfile', verbose_name='\u8bbe\u5907\u63cf\u8ff0'),
        ),
        migrations.AddField(
            model_name='device',
            name='users',
            field=models.ManyToManyField(to='users.User', verbose_name='\u6240\u5c5e\u7528\u6237'),
        ),
        migrations.AddField(
            model_name='customfields',
            name='device',
            field=models.OneToOneField(null=True, blank=True, to='device.Device', verbose_name='\u81ea\u5b9a\u4e49\u5b57\u6bb5'),
        ),
    ]
