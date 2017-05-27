# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='PopulationExplorer API')


urlpatterns = [
    url(r'doc/$', schema_view),
    url(r'rest-auth/', include('rest_auth.urls')),
    #url(r'users/', include('leisure-search.users.api_urls')),
]