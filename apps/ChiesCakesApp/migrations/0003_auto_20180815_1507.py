# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-15 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChiesCakesApp', '0002_reviews_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='picture',
            field=models.TextField(),
        ),
    ]
