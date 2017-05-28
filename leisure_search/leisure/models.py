# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from leisure_search.users.utils import LIKE_RATING_CHOICES

from model_utils.models import TimeStampedModel


def institution_photo_directory_path(instance, filename):
    return 'photos/{0}/{1}'.format(instance.name, filename)


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


@python_2_unicode_compatible
class Like(TimeStampedModel):

    rank = models.PositiveSmallIntegerField('Like type', choices=LIKE_RATING_CHOICES,
                                            default=LIKE_RATING_CHOICES.ONE)
    user = models.ForeignKey('users.User', related_name='likes', null=True, on_delete=models.SET_NULL)
    institution = models.ForeignKey(Institution, related_name='likes', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return "{}_{}".format(self.user.get_short_name(), self.created)


@python_2_unicode_compatible
class Stat(TimeStampedModel):

    rank_for_search = models.PositiveSmallIntegerField('Like search type', choices=LIKE_RATING_CHOICES,
                                            default=LIKE_RATING_CHOICES.ONE)
    user = models.ForeignKey('users.User', related_name='stats', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, related_name='stats', null=True, on_delete=models.SET_NULL)

    latitude_start_search = models.DecimalField(max_digits=19, decimal_places=10, default=0)
    longitude_start_search = models.DecimalField(max_digits=19, decimal_places=10, default=0)

    class Meta:
        verbose_name = 'Stat'
        verbose_name_plural = 'Stats'

    def __str__(self):
        return "{}_{}_{}".format(self.user.get_short_name(), self.created, self.rank_for_search)