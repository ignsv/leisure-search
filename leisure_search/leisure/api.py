# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.http import Http404
from django.db.models import Q, When, Case, Value, BooleanField, Count, CharField
from django.utils.translation import ugettext as _

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin

from .serializers import CategorySimpleSerializer, InstitutionCreateSerializer, InstitutionRetrieveSerializer, \
    CitySimpleSerializer, StatInstitutionCloserCreateSerializer

#from .permissions import CompanyOwnerPermission, UserOfferPermission

Category = apps.get_model('leisure', 'Category')
City = apps.get_model('leisure', 'City')
Institution = apps.get_model('leisure', 'Institution')


class CityApiView(ListAPIView):
    """
    ## Retrieve City list
    ####**Allowed Methods**:
    ###### - GET

    #### **GET**:
    ###### URL: **/api/leisure/city/**
    #### **SUCCESSFUL RESPONSE**:
    ```json
        {
          "count": 1,
          "next": null,
          "previous": null,
          "results": [
            {
              "id": 1,
              "name": "Kiev"
            }
          ]
        }
        <*status code:* 200>
    ```
    <*status code:* 200>
    """
    serializer_class = CitySimpleSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user': self.request.user,
        }

    def get_queryset(self):
        return City.objects.all()

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryApiView(RetrieveModelMixin, ListModelMixin, GenericViewSet):

    serializer_class = CategorySimpleSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user': self.request.user,
        }

    def get_queryset(self):
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        """
        ## Retrieve Category list
        ####**Allowed Methods**:
        ###### - GET

        #### **GET**:
        ###### URL: **/api/leisure/category/**
        #### **SUCCESSFUL RESPONSE**:
        ```json
            {
              "count": 1,
              "next": null,
              "previous": null,
              "results": [
                {
                  "id": 1,
                  "name": "cafe"
                }
              ]
            }
            <*status code:* 200>
        ```
        <*status code:* 200>
        """

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        ## Retrieve Category
        ####**Allowed Methods**:
        ###### - GET

        #### **GET**:
        ###### URL: **api/leisure/category/{category_pk}**
        #### **SUCCESSFUL RESPONSE**:
        ```json
            {
                "id": 1,
                "name": "cafe"
            }
            <*status code:* 200>
        ```
        <*status code:* 200>
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)


class InstitutionApiView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
#class InstitutionApiView(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):

    serializer_class = InstitutionRetrieveSerializer
    create_serializer = InstitutionCreateSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user': self.request.user,
        }

    def get_queryset(self):
        return Institution.objects.filter(published=True)

    def list(self, request, *args, **kwargs):
        """
        ## Retrieve Institution list
        ####**Allowed Methods**:
        ###### - GET

        #### **GET**:
        ###### URL: **/api/leisure/institution/**
        #### **SUCCESSFUL RESPONSE**:
        ```json
            {
              "count": 1,
              "next": null,
              "previous": null,
              "results": [
                {
                  "id": 2,
                  "name": "Francua",
                  "photo": "http://localhost:8000/media/photos/Francua/burjak4.jpg",
                  "city": {
                    "id": 1,
                    "name": "Kiev"
                  },
                  "address": "Kiev, Kiev",
                  "categories": [
                    {
                      "id": 1,
                      "name": "cafe"
                    }
                  ],
                  "latitude": "0.0000000000",
                  "longitude": "0.0000000000"
                }
              ]
            }
            <*status code:* 200>
        ```
        <*status code:* 200>
        """

        return super(InstitutionApiView, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        ## Retrieve Institution
        ####**Allowed Methods**:
        ###### - GET

        #### **GET**:
        ###### URL: **api/leisure/category/{institution_pk}**
        #### **SUCCESSFUL RESPONSE**:
        ```json
            {
              "id": 2,
              "name": "Francua",
              "photo": "http://localhost:8000/media/photos/Francua/burjak4.jpg",
              "city": {
                "id": 1,
                "name": "Kiev"
              },
              "address": "Kiev, Kiev",
              "categories": [
                {
                  "id": 1,
                  "name": "cafe"
                }
              ],
              "latitude": "0.0000000000",
              "longitude": "0.0000000000"
            }
            <*status code:* 200>
        ```
        <*status code:* 200>
        """
        return super(InstitutionApiView, self).retrieve(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #
    #     serializer = self.create_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     retrieve_serializer = self.serializer_class(data=serializer.data)
    #     return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    #     #return super(InstitutionApiView, self).create(request, *args, **kwargs)


class CloserInstitutionApiView(CreateAPIView):
    """
        **Search closer institution by rank and category**

        **Required data**
        <pre>
            {
            "rank_for_search": *int* 1-5,
            "category": *int*,fk for category
            "latitude_start_search": *decimal*,
            "longitude_start_search": *decimal*
            }
        </pre>

        **Success:** status_code: 200
        <pre>
            {
                "id": 5,
                "name": "Francua",
                "photo": "/media/photos/burjak3.jpg",
                "city": {
                    "id": 1,
                    "name": "Kiev"
                },
                "address": "Kiev, Kiev",
                "categories": [
                    {
                        "id": 1,
                        "name": "cafe"
                    }
                ],
                "latitude": "0.0000000000",
                "longitude": "0.0000000000"
            }
        </pre>

        **Error:** status_code: 400

        *Non-field errors*:
        <pre>
            {
                "non_field_errors": [
                    "Validation errors"
                ]
            }
        </pre>

        *Field errors*:
        <pre>
            {
                "rank_for_search": [
                    "Rank must be in 1-5!"
                ],
                "category": [
                    "No category in request"
                ],
            }
        </pre>

        """

    serializer_class = StatInstitutionCloserCreateSerializer
    permission_classes = (IsAuthenticated,)
    institution_retrieve = InstitutionRetrieveSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user': self.request.user,
        }

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = request.data
        # TODO search intitution
        institution = Institution.objects.first()
        if institution:
            return_serializer = self.institution_retrieve(institution)
            return Response(return_serializer.data, status=status.HTTP_200_OK, headers=headers)

        return Response("No institution for return", status=status.HTTP_200_OK, headers=headers)
