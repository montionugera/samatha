# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-24 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsuite', '0002_auto_20170228_0546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='epictestcase',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='epictestcase',
            name='key',
            field=models.CharField(default=None, max_length=128, unique=True),
            preserve_default=False,
        ),
    ]
