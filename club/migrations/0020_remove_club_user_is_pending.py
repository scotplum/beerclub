# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-06 16:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0019_auto_20171006_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club_user',
            name='is_pending',
        ),
    ]
