# -*- coding: utf-8 -*-

from django.conf.urls import url

from leisure_search.users import api

urlpatterns = [
    url(r'^register/$', api.UserSignUpAPIView.as_view(), name='api_user_signup'),
]
