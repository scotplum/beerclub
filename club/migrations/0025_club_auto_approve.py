# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-01-08 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0024_auto_20180108_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='auto_approve',
            field=models.BooleanField(default=False),
        ),
    ]
