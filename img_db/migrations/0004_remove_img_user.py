# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-05-01 11:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('img_db', '0003_img_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='img',
            name='user',
        ),
    ]
