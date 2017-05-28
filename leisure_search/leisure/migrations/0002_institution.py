# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-28 10:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import leisure_search.leisure.models
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leisure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
                ('photo', models.ImageField(upload_to=leisure_search.leisure.models.institution_photo_directory_path, verbose_name='Photo')),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('published', models.BooleanField(default=False)),
                ('latitude', models.DecimalField(decimal_places=10, default=0, max_digits=19)),
                ('longitude', models.DecimalField(decimal_places=10, default=0, max_digits=19)),
                ('categories', models.ManyToManyField(related_name='institutions', to='leisure.Category', verbose_name='Categories')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institutions', to='leisure.City')),
            ],
            options={
                'verbose_name': 'Institution',
                'verbose_name_plural': 'institutions',
            },
        ),
    ]
