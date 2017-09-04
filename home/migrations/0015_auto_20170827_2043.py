# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-28 01:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0014_beer_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer_Head',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bdb_id', models.CharField(max_length=20)),
                ('persistent', models.BooleanField(default=False)),
                ('rocky', models.BooleanField(default=False)),
                ('large', models.BooleanField(default=False)),
                ('fluffy', models.BooleanField(default=False)),
                ('dissipating', models.BooleanField(default=False)),
                ('lingering', models.BooleanField(default=False)),
                ('white', models.BooleanField(default=False)),
                ('offwhite', models.BooleanField(default=False)),
                ('tan', models.BooleanField(default=False)),
                ('frothy', models.BooleanField(default=False)),
                ('delicate', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='beer_color',
            name='delicate',
        ),
        migrations.RemoveField(
            model_name='beer_color',
            name='dissipating',
        ),
        migrations.RemoveField(
            model_name='beer_color',
            name='fluffy',
        ),
        migrations.RemoveField(
            model_name='beer_color',
            name='frothy',
        ),
        migrations.RemoveField(
            model_name='beer_color',
            name='large',
        ),
        migrations.RemoveField(
            model_name='beer_color',
            name='lingering',
        ),
        migrations.RemoveField(
            model_name='beer_color',
            name='offwhite',
        ),
        migrations.RemoveField(
            model_name='beer_color',
            name='persistent',
        ),
        migrations.RemoveField(
            model_name='beer_color',
            name='rocky',
        ),
        migrations.RemoveField(
            model_name='beer_color',
            name='tan',
        ),
        migrations.RemoveField(
            model_name='beer_color',
            name='white',
        ),
    ]