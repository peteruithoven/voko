# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-17 09:42


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0014_auto_20160617_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='mollie_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
