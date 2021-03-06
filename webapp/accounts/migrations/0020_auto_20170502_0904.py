# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-02 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20160315_1106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'adres', 'verbose_name_plural': 'adressen'},
        ),
        migrations.AlterModelOptions(
            name='emailconfirmation',
            options={'verbose_name': 'emailbevestiging', 'verbose_name_plural': 'emailbevestigingen'},
        ),
        migrations.AlterModelOptions(
            name='passwordresetrequest',
            options={'verbose_name': 'wachtwoordreset-aanvraag', 'verbose_name_plural': 'wachtwoordreset-aanvragen'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'ledenprofiel', 'verbose_name_plural': 'ledenprofielen'},
        ),
        migrations.AlterModelOptions(
            name='vokouser',
            options={'verbose_name': 'lid', 'verbose_name_plural': 'leden'},
        ),
        migrations.AlterField(
            model_name='vokouser',
            name='email',
            field=models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='E-mail adres'),
        ),
        migrations.AlterField(
            model_name='vokouser',
            name='is_asleep',
            field=models.BooleanField(default=False, verbose_name='Sleeping (inactive) member'),
        ),
    ]
