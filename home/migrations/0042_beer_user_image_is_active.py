# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-19 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_auto_20180216_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer_user_image',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
