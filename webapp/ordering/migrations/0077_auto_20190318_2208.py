# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-18 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0076_auto_20190308_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderround',
            name='closed_for_orders',
            field=models.DateTimeField(help_text='When this order round will close', unique=True),
        ),
        migrations.AlterField(
            model_name='orderround',
            name='collect_datetime',
            field=models.DateTimeField(help_text='When the products can be collected', unique=True),
        ),
        migrations.AlterField(
            model_name='orderround',
            name='open_for_orders',
            field=models.DateTimeField(help_text='When this order round will open', unique=True),
        ),
    ]
