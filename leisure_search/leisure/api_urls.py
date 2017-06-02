# -*- coding: utf-8 -*-

from django.conf.urls import url

from leisure_search.leisure import api

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'category', api.CategoryApiView, base_name='api_leisure_category')
router.register(r'institution', api.InstitutionApiView, base_name='api_leisure_institution')

urlpatterns = [
    url(r'^city/list$', api.CityApiView.as_view(), name='api_leisure_city'),
    url(r'^search/closer$', api.CloserInstitutionApiView.as_view(), name='api_search_closer'),
    url(r'^search/radius', api.RadiusInstitutionApiView.as_view(), name='api_search_radius'),
    url(r'^create/like$', api.LikeCreateApiView.as_view(), name='api_create_like'),
]

urlpatterns += router.urls
