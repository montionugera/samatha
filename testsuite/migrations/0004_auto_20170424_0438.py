# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-24 04:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testsuite', '0003_auto_20170424_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='epictestsuite',
            name='created_dttm',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='epictestsuite',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='testsuite_epictestsuite_creator_related', related_query_name='testsuite_epictestsuites_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='epictestsuite',
            name='update_dttm',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
