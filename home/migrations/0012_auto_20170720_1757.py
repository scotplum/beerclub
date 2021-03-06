# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-20 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_beer_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer_note',
            name='beer_category',
            field=models.CharField(default='Test Category', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='beer_note',
            name='beer_company',
            field=models.CharField(default='Test Company', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='beer_note',
            name='beer_name',
            field=models.CharField(default='Test Beer', max_length=500),
            preserve_default=False,
        ),
    ]
