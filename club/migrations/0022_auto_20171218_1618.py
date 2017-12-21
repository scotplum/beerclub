# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-18 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0021_auto_20171217_1430'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='club_user',
            options={'ordering': ['user__username']},
        ),
        migrations.AddField(
            model_name='club',
            name='display_wanted_beer',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
