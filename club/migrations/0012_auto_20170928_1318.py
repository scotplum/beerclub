# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-28 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0011_auto_20170926_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='bio',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='club_announcement',
            name='announcement',
            field=models.TextField(max_length=1000),
        ),
    ]
