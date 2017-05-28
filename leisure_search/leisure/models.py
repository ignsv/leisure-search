from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from model_utils.models import TimeStampedModel
from model_utils.choices import Choices


def institution_photo_directory_path(instance, filename):
    return 'photos/{0}/{1}'.format(instance.id, filename)


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


@python_2_unicode_compatible
class Institution(TimeStampedModel):

    name = models.CharField(max_length=255)
    photo = models.ImageField(verbose_name='Photo', upload_to=institution_photo_directory_path,)
    city = models.ForeignKey(City, related_name='institutions', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    categories = models.ManyToManyField('leisure.Category', verbose_name='Categories', related_name='institutions')
    published = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=19, decimal_places=10, default=0)
    longitude = models.DecimalField(max_digits=19, decimal_places=10, default=0)

    class Meta:
        verbose_name = 'Institution'
        verbose_name_plural = 'institutions'

    def __str__(self):
        return self.name

