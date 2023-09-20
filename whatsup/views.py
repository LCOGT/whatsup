"""
WhatsUP: astronomical object suggestions for Las Cumbres Observatory Global Telescope Network
Copyright (C) 2014-2015 LCOGT

views.py - data wrangling for templates

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework_jsonp.renderers import JSONPRenderer

from whatsup.models import Target
from whatsup.serializers import TargetSerializerQuerystring, \
    AdvTargetSerializer, RangeTargetSerializerQuerystring
from .utils import search_targets, range_targets

import logging

logger = logging.getLogger(__name__)

coords = settings.COORDS


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'search': reverse('api_search', request=request, format=format),
    })

class TargetDetailView(APIView):
    """
    Returns a match for Target name with filter and suggested exp times:
    * name (required) - name of the object
    * aperture (required) - One of '0m4', '1m0','2m0'
    """
    renderer_classes = (JSONRenderer, JSONPRenderer, BrowsableAPIRenderer)

    def get(self, request, format=None):
        name = request.query_params.get('name',None)
        name = name.replace(' ','').upper()
        targets = Target.objects.filter(name=name)
        aperture = request.query_params.get('aperture',None)
        tgs = filter_targets_with_aperture(targets, aperture=aperture, mode=None)
        serializer = AdvTargetSerializer(tgs, many=True)
        if serializer.data:
            data = serializer.data[0]
        else:
            data = []
        content = {'target': data,
                    'aperture' : aperture,
                   }
        return Response(content)

class TargetFullListView(APIView):
    """
    Returns the full list of Targets
    """
    renderer_classes = (JSONRenderer, JSONPRenderer, BrowsableAPIRenderer)

    def get(self, request, format=None):
        targets = targets_all()
        serializer = AdvTargetSerializer(targets, many=True)
        content = {'targets': serializer.data,
                   'count' : len(targets)}
        return Response(content)

class TargetListView(APIView):
    """
    Returns the list of Targets with filters applied:
    * start (required) - YYYY-MM-DDTHH:MM:SS
    * site (required) - LCO 3-letter site code
    * aperture (required) - LCO 3-letter telescope class
    * mode (optional) - Values are 'full', 'best', 'rti', 'messier'
    * category (optional) - filter by AVM category of target
    """
    renderer_classes = (JSONRenderer, JSONPRenderer, BrowsableAPIRenderer)

    def get(self, request, format=None):
        ser = TargetSerializerQuerystring(data=request.query_params)
        if not ser.is_valid(raise_exception=True):
            logger.error(ser.errors)
        targets = search_targets(request.query_params)
        serializer = AdvTargetSerializer(targets, many=True)
        content = {'targets': serializer.data,
                   'site': request.query_params.get('site', ''),
                   'datetime': request.query_params.get('start', ''),
                   'count' : len(targets)}
        return Response(content)

    def post(self, request, format=None):
        serializer = AdvTargetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TargetListRangeView(APIView):
    """
    Return targets visible in northern and southern hemisphere during time range
        * start (required) - YYYY-MM-DDTHH:MM:SS
        * end (required) - YYYY-MM-DDTHH:MM:SS
        * aperture (required) - LCO 3-letter telescope class
        * mode (optional) - Values are 'full', 'best', 'rti', 'messier'
        * category (optional) - filter by AVM category of target
    """
    renderer_classes = (JSONRenderer, JSONPRenderer, BrowsableAPIRenderer)

    def get(self, request, format=None):
        ser = RangeTargetSerializerQuerystring(data=request.query_params)
        if not ser.is_valid(raise_exception=True):
            logger.error(ser.errors)
        targets = range_targets(request.query_params)
        serializer = AdvTargetSerializer(targets, many=True)
        content = {'targets': serializer.data,
                   'site': request.query_params.get('site', ''),
                   'datetime': request.query_params.get('start', ''),
                   'count' : len(targets)}
        return Response(content)


