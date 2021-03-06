# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-15 10:06


from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0004_auto_20141205_1216'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventlog',
            options={},
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]
