# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-29 09:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0007_auto_20191029_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='url_name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
