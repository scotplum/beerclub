# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-05 15:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0045_auto_20180301_1523'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Beer_Category',
        ),
    ]
