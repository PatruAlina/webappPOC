# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 09:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pentagram', '0006_auto_20160919_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='like',
        ),
    ]