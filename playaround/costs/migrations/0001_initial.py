# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import costs.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=50, verbose_name=b'Cost number')),
                ('image', models.FileField(null=True, upload_to=costs.models.generate_cost_name, blank=True)),
                ('description', models.TextField(blank=True)),
                ('amount', models.DecimalField(null=True, verbose_name='Total amount', max_digits=40, decimal_places=2, blank=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CostLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(null=True, max_digits=40, decimal_places=2, blank=True)),
                ('tax_rate', models.DecimalField(null=True, max_digits=40, decimal_places=2, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cost', models.ForeignKey(related_name='cost_lines', to='costs.Cost')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
