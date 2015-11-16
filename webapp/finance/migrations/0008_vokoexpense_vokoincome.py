# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0053_auto_20151021_2043'),
        ('finance', '0007_auto_20150719_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='VokoExpense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('description', models.TextField()),
                ('order_round', models.ForeignKey(related_name='', blank=True, to='ordering.OrderRound', help_text=b'Optionally link to order round', null=True)),
                ('supplier', models.ForeignKey(related_name='', blank=True, to='ordering.Supplier', help_text=b'Optionally link to supplier', null=True)),
                ('user_balance', models.OneToOneField(related_name='', null=True, blank=True, to='finance.Balance', help_text=b'User balance, if any')),
            ],
            options={
                'verbose_name': 'Uitgave',
                'verbose_name_plural': 'Uitgaven',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VokoIncome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('description', models.TextField()),
                ('order_round', models.ForeignKey(related_name='', blank=True, to='ordering.OrderRound', help_text=b'Optionally link to order round', null=True)),
                ('supplier', models.ForeignKey(related_name='', blank=True, to='ordering.Supplier', help_text=b'Optionally link to supplier', null=True)),
                ('user_balance', models.OneToOneField(related_name='', null=True, blank=True, to='finance.Balance', help_text=b'User balance, if any')),
            ],
            options={
                'verbose_name': 'Inkomste',
                'verbose_name_plural': 'Inkomsten',
            },
            bases=(models.Model,),
        ),
    ]
