"""
WhatsUP: astronomical object suggestions for Las Cumbres Observatory Global Telescope Network
Copyright (C) 2014-2015 LCOGT

urls.py

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
from rest_framework import serializers

from models import Target, Params, APERTURES


class FilterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='filters')

    class Meta:
        model = Params
        fields = ('exposure', 'name')


class AdvTargetSerializer(serializers.ModelSerializer):
    desc = serializers.CharField(source='description')
    avmcode = serializers.CharField(source='avm_code')
    avmdesc = serializers.CharField(source='avm_desc')
    filters = FilterSerializer(many=True, source='parameters')

    class Meta:
        model = Target
        fields = ('name', 'ra', 'dec', 'desc', 'filters', 'avmdesc', 'avmcode')

    def create(self, validated_data):
        params_data = validated_data.pop('params')
        target = Target.objects.create(**validated_data)
        for param_data in params_data:
            Params.objects.create(target=target, **param_data)
        return target


class TargetSerializer(serializers.ModelSerializer):
    desc = serializers.CharField(source='description')
    avmcode = serializers.CharField(source='avm_code')
    avmdesc = serializers.CharField(source='avm_desc')
    exp = serializers.CharField(source='exposure')

    class Meta:
        model = Target
        fields = ('name', 'ra', 'dec', 'filters', 'exp', 'desc', 'avmdesc', 'avmcode', 'aperture')

    def create(self, validated_data):
        params_data = validated_data.pop('params')
        target = Target.objects.create(**validated_data)
        for param_data in params_data:
            Params.objects.create(target=target, **param_data)
        return target


coords = settings.COORDS

sites = [(name, name) for name in coords.keys()]


class TargetSerializerQuerystring(serializers.Serializer):
    """
    This serializer is only used to validate querystring parameters in the api.
    """
    site = serializers.ChoiceField(choices=sites, required=False)
    start = serializers.DateTimeField()
    end = serializers.DateTimeField(required=False)
    aperture = serializers.ChoiceField(required=False, choices=APERTURES)
    full = serializers.ChoiceField(required=False, choices=(('true', ''), ('false', ''), ('messier', '')))

    def is_valid(self, raise_exception=True):
        super(TargetSerializerQuerystring, self).is_valid(raise_exception)
        if self.data.get('site', '') and not self.data.get('start', ''):
            raise serializers.ValidationError("You must provide start date/time and a site.")
        elif self.data.get('start', '') and not self.data.get('end', '') and not self.data.get('site', ''):
            raise serializers.ValidationError("You must provide an end date/time.")
