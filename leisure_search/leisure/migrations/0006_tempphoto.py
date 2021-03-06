# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-03 13:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import leisure_search.leisure.models
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leisure', '0005_auto_20170603_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('photo', models.ImageField(upload_to=leisure_search.leisure.models.institution_photo_directory_path, verbose_name='Photo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
