# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-16 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0040_beer_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer_user_image',
            name='description',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]