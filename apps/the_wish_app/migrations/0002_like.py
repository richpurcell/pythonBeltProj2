# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-26 00:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_wish_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wish_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]
