# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-11 10:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20170511_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='hairnownow',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='hairnownow_value',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='hairnymph',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='hairnymph_value',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='molatoo_lotion',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='molatoo_lotion_value',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='molatoo_serum',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='molatoo_serum_value',
        ),
    ]