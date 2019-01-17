# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-07 14:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryPersonCash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_person', models.CharField(default=b'', max_length=100)),
                ('count', models.IntegerField(blank=True, default=0)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('total', models.IntegerField(blank=True, default=0)),
            ],
        ),
    ]