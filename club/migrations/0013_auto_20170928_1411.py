# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-28 19:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0012_auto_20170928_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club_announcement',
            name='date_added',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]
