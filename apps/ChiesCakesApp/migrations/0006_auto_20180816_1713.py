# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-17 00:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChiesCakesApp', '0005_auto_20180815_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flavors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor', models.TextField()),
                ('img_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(),
        ),
    ]
