# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-04 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_event_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_address',
            name='google_maps',
            field=models.URLField(verbose_name='google maps'),
        ),
    ]
