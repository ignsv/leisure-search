# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-02 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leisure', '0003_like_stat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='rank',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Zero'), (1, 'One'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five')], default=0, verbose_name='Like type'),
        ),
        migrations.AlterField(
            model_name='stat',
            name='rank_for_search',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Zero'), (1, 'One'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five')], default=0, verbose_name='Like search type'),
        ),
    ]
