# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-16 19:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0003_auto_20170716_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club_Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement', models.CharField(max_length=1000)),
                ('is_active', models.BooleanField(default=True)),
                ('expiration_date', models.DateTimeField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.Club')),
            ],
        ),
    ]