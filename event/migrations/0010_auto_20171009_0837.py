# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-09 13:37
from __future__ import unicode_literals

from django.db import migrations, models
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_event_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_address',
            name='city',
            field=models.CharField(max_length=64, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='event_address',
            name='state',
            field=localflavor.us.models.USStateField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='event_address',
            name='zip_code',
            field=localflavor.us.models.USZipCodeField(blank=True, max_length=10, null=True),
        ),
    ]