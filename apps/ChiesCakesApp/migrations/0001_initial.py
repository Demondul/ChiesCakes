# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-29 19:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.CharField(max_length=255)),
                ('filename', models.CharField(max_length=255)),
                ('caption', models.CharField(max_length=255)),
                ('context', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=255)),
                ('contact_type', models.CharField(max_length=255)),
                ('isPrimary', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flavors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor', models.TextField()),
                ('img_url', models.CharField(max_length=255)),
                ('filename', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.CharField(max_length=255)),
                ('filename', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderType', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('quantity', models.IntegerField(default=1)),
                ('celebrant', models.CharField(max_length=255)),
                ('contact_number', models.CharField(blank=True, default=None, max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventType', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('event_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.TextField()),
                ('review', models.TextField()),
                ('rating', models.IntegerField(default=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email_address', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=25)),
                ('access_type', models.CharField(max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='reviews',
            name='review_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_reviews', to='ChiesCakesApp.Users'),
        ),
        migrations.AddField(
            model_name='reservations',
            name='event_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserves', to='ChiesCakesApp.Users'),
        ),
        migrations.AddField(
            model_name='orders',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='ChiesCakesApp.Reservations'),
        ),
        migrations.AddField(
            model_name='orders',
            name='order_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='ChiesCakesApp.Users'),
        ),
        migrations.AddField(
            model_name='comments',
            name='comment_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_comments', to='ChiesCakesApp.Users'),
        ),
        migrations.AddField(
            model_name='comments',
            name='comment_in',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='the_comments', to='ChiesCakesApp.Reviews'),
        ),
    ]
