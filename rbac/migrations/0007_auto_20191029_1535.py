# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-10-29 07:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0006_permission_parent_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='permission',
            old_name='parent_id',
            new_name='parent',
        ),
    ]
