# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-04 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0037_remove_beer_beer_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='beer_image_url',
            field=models.URLField(blank=True, max_length=250),
        ),
    ]
