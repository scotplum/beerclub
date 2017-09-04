# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-04 01:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0015_auto_20170827_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer_Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Beer_Attribute_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Beer_Attribute_Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Beer_Attribute_Category')),
            ],
        ),
        migrations.CreateModel(
            name='Profile_Sheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bdb_id', models.CharField(max_length=20)),
                ('beer_attribute', models.ManyToManyField(blank=True, to='home.Beer_Attribute')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='beer_attribute',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Beer_Attribute_Section'),
        ),
    ]