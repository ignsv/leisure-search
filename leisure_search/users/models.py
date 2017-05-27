# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.http import urlquote

from model_utils.models import TimeStampedModel
from model_utils.choices import Choices


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Create and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):
    """
     A fully featured User model with admin-compliant permissions that uses
     a full-length email field as the username.

     Email and password are required. Other fields are optional.
     """
    GENDER_TYPE_CHOICES = Choices(
        (0, 'MALE', 'Male',),
        (1, 'FEMALE', 'Female',),
    )

    username = models.CharField('Username', max_length=254, blank=True, null=True)
    email = models.EmailField('email address', max_length=254, unique=True, blank=True)
    first_name = models.CharField('first name', max_length=255, blank=True, null=True)
    last_name = models.CharField('last name', max_length=255, blank=True, null=True)
    birth_date = models.DateField('Birth Date', null=True)
    gender = models.PositiveSmallIntegerField('Gender type', choices=GENDER_TYPE_CHOICES,
                                              default=GENDER_TYPE_CHOICES.MALE)

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as '
                  'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = CustomUserManager()
    backend = 'django.contrib.auth.backends.ModelBackend'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self):
        return "{}".format(self.get_full_name() or self.email)
