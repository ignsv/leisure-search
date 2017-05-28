# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
import decimal
from django.apps import apps
from rest_framework import serializers

Category = apps.get_model('leisure', 'Category')
City = apps.get_model('leisure', 'City')
Institution = apps.get_model('leisure', 'Institution')


class CategorySimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)


class CitySimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'name',)


class InstitutionRetrieveSerializer(serializers.ModelSerializer):

    categories = CategorySimpleSerializer(many=True)
    city = CitySimpleSerializer(read_only=True)

    class Meta:
        model = Institution
        fields = ('id', 'name', 'photo', 'city', 'address', 'categories', 'latitude', 'longitude', )


class InstitutionCreateSerializer(serializers.ModelSerializer):

    city_id = serializers.IntegerField(required=True)
    latitude = serializers.DecimalField(required=True, decimal_places=10, max_digits=19)
    longitude = serializers.DecimalField(required=True, decimal_places=10, max_digits=19)

    class Meta:
        model = Institution
        fields = ('name', 'city_id', 'categories', 'latitude', 'longitude')

    def validate_city_id(self, value):
        if not City.objects.filter(id=value).exists():
            raise serializers.ValidationError('This city does not exists!')
        return value

    def validate(self, attrs):

        return attrs

    def create(self, validated_data):
        data = copy.deepcopy(validated_data)
        city = City.objects.get(pk=validated_data['city_id'])
        categories_ids = data.get('categories')
        del data['categories']
        data['city'] = city
        institution = Institution.objects.create(**data)
        institution.categories = categories_ids
        institution.save()
        return institution
