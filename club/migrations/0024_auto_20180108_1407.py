# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-01-08 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0023_auto_20180108_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='state',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
