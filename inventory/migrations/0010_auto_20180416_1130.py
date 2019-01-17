# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-16 11:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_category_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='flattummy',
            new_name='cocoa_my_koko',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='flattummy_value',
            new_name='cocoa_my_koko_value',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='hairnownow',
            new_name='ginger_me',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='hairnownow_value',
            new_name='ginger_me_value',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='hairnymph',
            new_name='green_with_envy',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='hairnymph_value',
            new_name='green_with_envy_value',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='lotion',
            new_name='inighe',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='lotion_value',
            new_name='inighe_value',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='molatoo_lotion',
            new_name='la_vida_loca',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='molatoo_lotion_value',
            new_name='la_vida_loca_value',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='molatoo_serum',
            new_name='nutty_by_nature',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='molatoo_serum_value',
            new_name='nutty_by_nature_value',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='serum',
            new_name='triple_threat',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='serum_value',
            new_name='triple_threat_value',
        ),
        migrations.RenameField(
            model_name='stockvalues',
            old_name='flattummy_value',
            new_name='cocoa_my_koko_value',
        ),
        migrations.RenameField(
            model_name='stockvalues',
            old_name='hairnownow_value',
            new_name='ginger_me_value',
        ),
        migrations.RenameField(
            model_name='stockvalues',
            old_name='hairnymph_value',
            new_name='green_with_envy_value',
        ),
        migrations.RenameField(
            model_name='stockvalues',
            old_name='lotion_value',
            new_name='inighe_value',
        ),
        migrations.RenameField(
            model_name='stockvalues',
            old_name='molatoo_lotion_value',
            new_name='la_vida_loca_value',
        ),
        migrations.RenameField(
            model_name='stockvalues',
            old_name='molatoo_serum_value',
            new_name='nutty_by_nature_value',
        ),
        migrations.RenameField(
            model_name='stockvalues',
            old_name='serum_value',
            new_name='triple_threat_value',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='shapeyou',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='shapeyou_value',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='slimcoffee',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='slimcoffee_value',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='slimtea',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='slimtea_value',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='soap',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='soap_value',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='spot_removal',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='spot_removal_value',
        ),
        migrations.RemoveField(
            model_name='stockvalues',
            name='shapeyou_value',
        ),
        migrations.RemoveField(
            model_name='stockvalues',
            name='slimcoffee_value',
        ),
        migrations.RemoveField(
            model_name='stockvalues',
            name='slimtea_value',
        ),
        migrations.RemoveField(
            model_name='stockvalues',
            name='soap_value',
        ),
        migrations.RemoveField(
            model_name='stockvalues',
            name='spot_removal_value',
        ),
    ]