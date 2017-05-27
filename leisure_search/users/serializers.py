# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
from leisure_search.users.utils import PASSWORD_FIELD_ERRORS
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.apps import apps
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):

    gender_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'birth_date', 'gender', 'gender_type')

    def get_gender_type(self, obj):
        return obj.get_gender_display()


class UserSignUpSerializer(serializers.ModelSerializer):

    password = serializers.CharField(required=True, min_length=8, error_messages=PASSWORD_FIELD_ERRORS)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'birth_date', 'gender', 'password',
        )

    def validate(self, attrs):
        email = attrs.get('email', None) or None
        if email is None:
            raise serializers.ValidationError('Email can not be blank')

        email = email.strip().lower()

        try:
            User.objects.get(email=email)
            raise serializers.ValidationError("User with this email already exists")
        except User.DoesNotExist:
            return attrs
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def create(self, validated_data):
        data = validated_data.copy()

        user_email = data.pop('email')
        user_password = data.pop('password')

        user = User.objects.create_user(email=user_email, username=user_email,
                                        password=user_password, **data)

        return user
