# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-11 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0010_auto_20171009_0837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='address',
        ),
        migrations.AddField(
            model_name='event_address',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='event.Event'),
            preserve_default=False,
        ),
    ]
