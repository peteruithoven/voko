# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-02 22:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0078_auto_20190319_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderround',
            name='distribution_coordinator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coordinating_distribution_orderrounds', to=settings.AUTH_USER_MODEL),
        ),
    ]
