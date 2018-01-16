# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceprofile',
            name='type',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u8bbe\u5907\u7c7b\u578b', choices=[(1, 'mac'), (2, 'Common'), (3, 'android')]),
        ),
    ]
