# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.http import Http404
from django.db.models import Q, When, Case, Value, BooleanField, Count, CharField
from django.utils.translation import ugettext as _

from django_filters.rest_framework import DjangoFilterBackend
from leisure_search.leisure.utils import return_list_of_distance
from rest_framework import filters
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from django.db.models.functions import Coalesce
from django.db.models import Sum, Value as V

from .serializers import CategorySimpleSerializer, InstitutionCreateSerializer, InstitutionRetrieveSerializer, \
    CitySimpleSerializer, StatInstitutionCloserCreateSerializer, LikeCreateSerializer, LikeRetrieveSerializer, \
    StatInstitutionRadiusCreateSerializer, UpdatePhotoInstituteSerializer, TempPhotoSerializer

#from .permissions import CompanyOwnerPermission, UserOfferPermission

Category = apps.get_model('leisure', 'Category')
City = apps.get_model('leisure', 'City')
Institution = apps.get_model('leisure', 'Institution')
TempPhoto = apps.get_model('leisure', 'TempPhoto')


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


class InstitutionApiView(RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):

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

    def get_serializer_class(self):
        if self.action=='create':
            return self.create_serializer
        return self.serializer_class

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
                  "photo": "http://localhost:8000/media/photos/dweew.jpg",
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
              "photo": "http://localhost:8000/media/photos/dwedwedwe.jpg",
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

    def create(self, request, *args, **kwargs):
        """
            **Create institution api view**

            **Required data**
            <pre>
                {
                    "name": *str*,
                    "city": *id*,
                    "address": "str", blank = True
                    "categories": [],
                    "latitude": decimal,
                    "longitude": decimal
                }
                example
                {
                    "name": "Cafe3",
                    "city": 1,
                    "address": "",
                    "categories": [1],
                    "latitude": 12.01,
                    "longitude": 12.01
                }
            </pre>

            **Success:** status_code: 201
            <pre>
                {
                    "id": 2,
                    "rank": 3,
                    "institution": {
                        "id": 5,
                        "name": "Francua",
                        "photo": "null",
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
                }
            </pre>

            **Error:** status_code: 400

            *Non-field errors*:
            <pre>
                {
                    "non_field_errors": [
                        "Validation errors",
                         "Some validation error,
                    ]
                }
            </pre>
        """
        return super(InstitutionApiView, self).create(request, *args, **kwargs)


class UpdatePhotoInstitutionApiView(UpdateAPIView):

    serializer_class = UpdatePhotoInstituteSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user': self.request.user,
        }

    def get_queryset(self):
        return Institution.objects.all()

    def update(self, request, *args, **kwargs):
        """
        ## Update Photo Institution
        ####**Allowed Methods**:
        ###### - PUT - PATCH

        #### **PATCH**:
        ###### URL: **/api/leisure/institution/{id}**

        #### **EXAMPLE REQUEST**:
        ```json
            {
                "temp_photo_id": "int"
            }
        ```

        #### **SUCCESSFUL RESPONSE**:
        ```json
            {
              "id": 2,
              "name": "Francua",
              "photo": "http://localhost:8000/media/photos/ewdwedw.jpg",
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

        return super(UpdatePhotoInstitutionApiView, self).update(request, *args, **kwargs)


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
                ""photo": "http://localhost:8000/media/photos/ewdewfer.jpg",
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
        data = serializer.validated_data
        # search intitution
        institution_queryset = Institution.objects.annotate(mean_rank=Coalesce(Avg('likes__rank'), V(0))).\
            filter(categories__in=[data['category'].id, ], mean_rank__gte=data['rank_for_search'], published=True)\
            .distinct()

        list_result = return_list_of_distance(data['latitude_start_search'], data['longitude_start_search'],
                                              institution_queryset)

        if list_result:
            return_serializer = self.institution_retrieve(list_result[0][0])
            return Response(return_serializer.data, status=status.HTTP_200_OK, headers=headers)

        return Response({"result": "No institution for return"}, status=status.HTTP_404_NOT_FOUND, headers=headers)


class LikeCreateApiView(CreateAPIView):
    """
        **Create like api view**

        **Required data**
        <pre>
            {
              "institution": "string",
              "rank": "string"
            }
        </pre>

        **Success:** status_code: 201
        <pre>
            {
                "id": 2,
                "rank": 3,
                "institution": {
                    "id": 5,
                    "name": "Francua",
                    "photo": "http://localhost:8000/media/photos/shoto.jpg",
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
            }
        </pre>

        **Error:** status_code: 400

        *Non-field errors*:
        <pre>
            {
                "non_field_errors": [
                    "Validation errors",
                     "You have already vote for this institution",
                ]
            }
        </pre>

        *Field errors*:
        <pre>
            {
                "rank_for_search": [
                    "Rank must be in 1-5!"
                ],
                "institution": [
                    "No institution in request"
                ],
            }
        </pre>

        """

    serializer_class = LikeCreateSerializer
    permission_classes = (IsAuthenticated,)

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

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RadiusInstitutionApiView(CreateAPIView):
    """
        **Search in radius institutions by rank and category**

        **Required data**
        <pre>
            {
            "radius": *float* in meters
            "rank_for_search": *int* 1-5,
            "category": *int*,fk for category
            "latitude_start_search": *decimal*,
            "longitude_start_search": *decimal*
            }
        </pre>

        **Success:** status_code: 200
        <pre>
        {
            "results": [
                7,
                5
                ...
            ]
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

    serializer_class = StatInstitutionRadiusCreateSerializer
    permission_classes = (IsAuthenticated,)
    institution_retrieve = InstitutionRetrieveSerializer

    def get_queryset(self):
        return None

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
        data = serializer.validated_data
        # search intitution
        institution_queryset = Institution.objects.annotate(mean_rank=Coalesce(Avg('likes__rank'), V(0))). \
            filter(categories__in=[data['category'].id, ], mean_rank__gte=data['rank_for_search'], published=True).\
            distinct()

        list_result = return_list_of_distance(data['latitude_start_search'], data['longitude_start_search'],
                                              institution_queryset)
        if list_result:
            institution_ids = [item[0].id for item in list_result if item[1]<data['radius']]
            return Response({"results": institution_ids}, status=status.HTTP_200_OK, headers=headers)

        return Response({"result": "No institution for return"}, status=status.HTTP_404_NOT_FOUND, headers=headers)


class CreateTempPhotoApiView(CreateAPIView):
    """
        **Create temp Photo instanse**

        **Required data**
        <pre>
            {
            "photo": *binary*
            }
        </pre>

        **Success:** status_code: 201
        <pre>
            {
            "id": *int*,
            "photo": *binary*
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
        """

    serializer_class = TempPhotoSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'user': self.request.user,
        }

    def create(self, request, *args, **kwargs):
        return super(CreateTempPhotoApiView,self).create(request, *args, **kwargs)
