# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-01-08 14:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0014_auto_20171018_1450'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['event_date']},
        ),
    ]