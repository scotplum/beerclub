# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-07 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apidata', '0002_beer_style'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer_style',
            name='abvMax',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='beer_style',
            name='abvMin',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='beer_style',
            name='description',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name='beer_style',
            name='fgMax',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='beer_style',
            name='fgMin',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='beer_style',
            name='ibuMax',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='beer_style',
            name='ibuMin',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='beer_style',
            name='ogMax',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='beer_style',
            name='ogMin',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='beer_style',
            name='srmMax',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='beer_style',
            name='srmMin',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]