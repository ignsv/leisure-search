# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
import decimal
from django.apps import apps
from rest_framework import serializers

Category = apps.get_model('leisure', 'Category')
City = apps.get_model('leisure', 'City')
Institution = apps.get_model('leisure', 'Institution')
Stat = apps.get_model('leisure', 'Stat')
Like = apps.get_model('leisure', 'Like')
TempPhoto = apps.get_model('leisure', 'TempPhoto')


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

    latitude = serializers.DecimalField(required=True, decimal_places=10, max_digits=19)
    longitude = serializers.DecimalField(required=True, decimal_places=10, max_digits=19)

    class Meta:
        model = Institution
        fields = ('name', 'city', 'address', 'categories', 'latitude', 'longitude')

    def validate_city(self, value):
        if not value:
            raise serializers.ValidationError('Enter city!')
        return value

    def validate_categories(self, value):
        if not value:
            raise serializers.ValidationError('Enter at least one category!')
        return value

    def validate(self, attrs):

        return attrs

    def create(self, validated_data):
        data = copy.deepcopy(validated_data)
        categories_ids = data.pop('categories')
        institution = Institution.objects.create(**data)
        institution.categories = categories_ids
        institution.save()
        return institution

    def to_representation(self, instance):
        retrieve_serializer = InstitutionRetrieveSerializer(instance)
        retrieve_serializer.context['request'] = self.context['request']
        return retrieve_serializer.data


class UpdatePhotoInstituteSerializer(serializers.ModelSerializer):
    """
    Add Photo to institution
    """
    temp_photo_id = serializers.IntegerField(required=True)

    class Meta:
        model = Institution
        fields = ('temp_photo_id', )

    def validate(self, attrs):

        if not self.partial:
            raise serializers.ValidationError('Only Patch method allowed!')

        temp_photo = TempPhoto.objects.filter(pk=attrs['temp_photo_id']).first()

        if not temp_photo:
            raise serializers.ValidationError('Please enter valide temp photo id')

        if self.instance:
            if self.instance.photo:
                raise serializers.ValidationError('Institution have already had photo!')
        return attrs

    def update(self, instance, validated_data):
        temp_photo = TempPhoto.objects.get(pk=validated_data['temp_photo_id'])
        instance.photo = temp_photo.photo
        temp_photo.delete()
        instance.save()

        return instance

    def to_representation(self, instance):

        retrieve_serializer = InstitutionRetrieveSerializer(instance)
        retrieve_serializer.context['request'] = self.context['request']
        return retrieve_serializer.data


class StatInstitutionSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stat
        fields = ('id', 'rank_for_search', 'user', 'category', 'latitude_start_search', 'longitude_start_search')


class StatInstitutionCloserCreateSerializer(serializers.ModelSerializer):

    latitude_start_search = serializers.DecimalField(required=True, decimal_places=10, max_digits=19)
    longitude_start_search = serializers.DecimalField(required=True, decimal_places=10, max_digits=19)

    class Meta:
        model = Stat
        fields = ('rank_for_search', 'category', 'latitude_start_search', 'longitude_start_search', )

    def validate_category(self, value):
        if value is None:
            raise serializers.ValidationError('No category in request')
        return value

    def validate_rank_for_search(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError('Rank must be in 1-5')
        return value

    def create(self, validated_data):

        data = copy.deepcopy(validated_data)
        data['user'] = self.context['request'].user

        instance = Stat.objects.create(**data)

        return instance


class StatInstitutionRadiusCreateSerializer(serializers.ModelSerializer):

    latitude_start_search = serializers.DecimalField(required=True, decimal_places=10, max_digits=19)
    longitude_start_search = serializers.DecimalField(required=True, decimal_places=10, max_digits=19)

    radius = serializers.FloatField(required=True)

    class Meta:
        model = Stat
        fields = ('rank_for_search', 'category', 'radius', 'latitude_start_search', 'longitude_start_search', )

    def validate_category(self, value):
        if value is None:
            raise serializers.ValidationError('No category in request')
        return value

    def validate_rank_for_search(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError('Rank must be in 1-5')
        return value

    def validate_radius(self, value):
        if value < 0:
            raise serializers.ValidationError('Radius less than 0')
        return value

    def create(self, validated_data):

        data = copy.deepcopy(validated_data)
        data['user'] = self.context['request'].user
        data.pop('radius')

        instance = Stat.objects.create(**data)

        return instance

    def to_representation(self, instance):
        return_serializer = StatInstitutionSimpleSerializer(instance)
        return_serializer.context['request'] = self.context['request']
        return return_serializer.data


class LikeRetrieveSerializer(serializers.ModelSerializer):

    institution = InstitutionRetrieveSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'rank', 'institution',)


class LikeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('rank', 'institution',)

    def validate_institution(self, value):
        if value is None:
            raise serializers.ValidationError('No institution in request')
        return value

    def validate_rank(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError('Rank must be in 1-5')
        return value

    def validate(self, attrs):

        if not attrs['institution'].published:
            raise serializers.ValidationError('This institution have not published yet')

        like = Like.objects.filter(user=self.context['request'].user, institution=attrs['institution']).first()

        if like:
            raise serializers.ValidationError('You have already vote for this institution')

        return attrs

    def create(self, validated_data):

        data = copy.deepcopy(validated_data)
        data['user'] = self.context['request'].user

        instance = Like.objects.create(**data)

        return instance

    def to_representation(self, instance):
        return_serializer = LikeRetrieveSerializer(instance)
        return_serializer.context['request'] = self.context['request']
        return return_serializer.data


class TempPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TempPhoto
        fields = ('id', 'photo',)
