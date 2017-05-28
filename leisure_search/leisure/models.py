from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from model_utils.models import TimeStampedModel
from model_utils.choices import Choices


@python_2_unicode_compatible
class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class City(models.Model):

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name
