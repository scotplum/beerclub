# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-01 21:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0044_beer_banner_beer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beer_banner',
            name='bdb_id',
        ),
        migrations.RemoveField(
            model_name='beer_banner',
            name='beer_website',
        ),
    ]
