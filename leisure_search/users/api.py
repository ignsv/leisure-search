# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login

from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status, permissions

from django.contrib.auth import get_user_model

from leisure_search.users import serializers

User = get_user_model()


class UserSignUpAPIView(CreateModelMixin, GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializers.UserDetailSerializer(instance=serializer.instance,
                                             context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED, headers=headers
        )

    def post(self, request, *args, **kwargs):
        """
        **Create User**

        ####**Allowed Methods**:
        ###### - POST

        #### **POST**:
        ###### URL: **users/register/**

        #### POST DATA:
        ```json
            {
            "email": "*str*",
            "first_name": "*str*",
            "last_name": "*str*",
            "birth_date": *str*,
            "gender": 0 - male, 1 - female,
            "password": "*str*"
            }
        ```

        #### SUCCESSFUL RESPONSE:
        ```json
            {
            "email": "ihnatenko@steelkiwi.com",
            "first_name": "Loh",
            "last_name": "pird",
            "birth_date": "2017-05-26",
            "gender": 1,
            "gender_type": "Female"
            }
            <*status code:* 201>
        ```

        #### FIELD ERROR RESPONSE:
        ```json
            {
              "user": {
                "email": [
                  "user with this email address already exists."
                ]
              }
            }
            <*status code:* 400>
        ```

        #### NON-FIELD ERROR RESPONSE:
        ```json
            {
              "non_field_errors": [
                "['Non-field error message']"
              ]
            }
            <*status code:* 400>
        ```
        """
        return self.create(request, *args, **kwargs)
