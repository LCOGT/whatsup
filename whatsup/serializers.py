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
from models import Target, APERTURES


# class LookupSerializer(serializers.Serializer):
# datetime = serializers.DateTimeField(required=True, validators=[validate_date,])
# enddate = serializers.DateTimeField(required=False)
#     aperture = serializers.CharField(required=False)
#     site = serializers.CharField()

#     def validate_date(value):
#         try:
#             value = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
#         except ValueError:
#             raise ValidationError("Date/time format must be YYYY-MM-DDTHH:MM:SS")
#         return value

#     def validate_site(value):
#         try:
#             site = settings.COORDS[value]
#         except KeyError:
#             raise ValidationError("Site provided is not official LCOGT site abbreviation. i.e. ogg, coj, cpt, lsc or elp")
#         return site

class TargetSerializer(serializers.ModelSerializer):
    exp = serializers.FloatField(source='exposure')
    desc = serializers.CharField(source='description')
    avmcode = serializers.CharField(source='avm_code')
    avmdesc = serializers.CharField(source='avm_desc')

    class Meta:
        model = Target
        fields = ('name', 'ra', 'dec', 'exp', 'desc', 'avmdesc', 'avmcode')

    def create(self, validated_data):
        target = Target.objects.create(**validated_data)
        return target

        # def update(self, instance, validated_data):
        #     """
        #     Update and return an existing `Target` instance, given the validated data.
        #     """
        #     instance.name = validated_data.get('name', instance.name)
        #     instance.ra = validated_data.get('ra', instance.ra)
        #     instance.dec = validated_data.get('dec', instance.dec)
        #     instance.exp = validated_data.get('exp', instance.exp)
        #     instance.desc = validated_data.get('desc', instance.desc)
        #     instance.avmdesc = validated_data.get('avmdesc', instance.avmdesc)
        #     instance.avmcode = validated_data.get('avmcode', instance.avmcode)

        #     instance.save()
        #     return instance

        # def init(self, *args, **kwargs):
        #     super(TargetSerializer, self).__init__(*args, **kwargs)
        #     self.fields['site'].validators.append(validate_site)
        #     self.fields['date'].validators.append(validate_date)


coords = settings.COORDS

sites = [(name, name) for name in coords.keys()]


class TargetSerializerQuerystring(serializers.Serializer):
    """
    This serializer is only used to validate querystring parameters in the api.
    """
    site = serializers.ChoiceField(choices=sites)
    datetime = serializers.DateTimeField()
    enddate = serializers.DateTimeField(required=False)
    aperture = serializers.ChoiceField(required=False, choices=APERTURES)
    full = serializers.ChoiceField(required=False, choices=(('true', ''), ('false', '')))
    callback = serializers.ChoiceField(required=False, choices=(('jsonp', ''),))
