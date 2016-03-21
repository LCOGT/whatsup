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
import json

import json
import pytest

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient

from .factories import TargetFactory
from ..models import Target

pytestmark = pytest.mark.django_db  # Explicit db access authorization


@pytest.fixture
def api_client():
    """ Fixture to bundle rest framework api client"""
    return APIClient()

@pytest.mark.django_db
class TestViews:
    pytestmark = pytest.mark.django_db
    def test_api_target_detail_get(api_client):
        target = TargetFactory.create(
            name="Gallifrey",
            ra=320.20,
            dec=54.20,
            description="From space, Gallifrey is seen as a yellow-orange planet",
            avm_desc="Gallifrey planet",
            avm_code="42"
        )
        response = api_client.get(reverse('api_target_detail', args=[target.pk]))
        assert response.status_code == 200
        assert response.data['name'] == "Gallifrey"
        assert response.data['ra'] == 320.20
        assert response.data['dec'] == 54.20
        assert response.data['exp'] == 0.0
        assert response.data['desc'] == "From space, Gallifrey is seen as a yellow-orange planet"
        assert response.data['avmdesc'] == "Gallifrey planet"
        assert response.data['avmcode'] == "42"


    def test_api_target_detail_put(api_client):
        data = {'name': "Gallifrey",
                'ra': 320.20,
                'dec': 54.20,
                'description': "From space, Gallifrey is seen as a yellow-orange planet",
                'avm_desc': "Gallifrey planet",
                'avm_code': "42", }
        target = TargetFactory.create(**data)

        new_data = {'name': "Gallifrey2",
                    'ra': 320.20,
                    'dec': 54.20,
                    'exp': 1,
                    'desc': "From space, Gallifrey is seen as a yellow-orange planet",
                    'avmdesc': "Gallifrey planet",
                    'avmcode': "42", }

        response = api_client.put(
            reverse('api_target_detail', args=[target.pk]),
            new_data
        )
        assert response.status_code == 200
        updated_target = Target.objects.get(pk=target.pk)
        assert updated_target.name == new_data['name']
        assert updated_target.description == new_data['desc']


    def test_api_target_detail_delete(api_client):
        data = {'name': "Tattooine",
                'ra': 130.0,
                'dec': 32.20,
                'description': "Tatooine is a desert planet in a binary star system",
                'avm_desc': "Tatooine planet",
                'avm_code': "2", }
        target = TargetFactory.create(**data)

        assert Target.objects.filter(pk=target.pk)

        response = api_client.delete(
            reverse('api_target_detail', args=[target.pk])
        )
        assert response.status_code == 204

        assert not Target.objects.filter(pk=target.pk)


    def test_api_search_page(api_client):
        TargetFactory.create_batch(30)  # We need at least 30 targets if the

        # Interval request
        response = api_client.get(
            '/search/',
            {'datetime': '2015-08-12T12:10:12', 'enddate': '2015-09-12T12:10:12', 'site': 'lsc'})
        assert response.status_code == 200

        # No enddate
        response = api_client.get(
            '/search/',
            {'datetime': '2015-08-12T12:10:12', 'site': 'lsc'})
        assert response.status_code == 200

        # With `aperture` parameter
        response = api_client.get(
            '/search/',
            {'datetime': '2015-08-12T12:10:12', 'site': 'lsc', 'aperture': '2m0'})
        assert response.status_code == 200

        # With `callback` parameter
        response = api_client.get(
            '/search/',
            {'datetime': '2015-08-12T12:10:12', 'site': 'lsc', 'callback': 'jsonp'})
        assert response.status_code == 200

        # Malformed datetime 1
        response = api_client.get(
            '/search/',
            {'datetime': '205-08-12T12:10:12', 'site': 'lsc'})
        assert response.status_code == 400
        assert len(response.data) == 1
        assert response.data['datetime'][0] == 'Datetime has wrong format. Use one of these formats instead:' \
                                               ' YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
        # Malformed datetime 2
        response = api_client.get(
            '/search/',
            {'datetime': '2015-08-12T27:10:12', 'site': 'lsc'})
        assert response.status_code == 400
        assert len(response.data) == 1
        assert response.data['datetime'][0] == 'Datetime has wrong format. Use one of these formats instead:' \
                                               ' YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'

        # Mandatory `datetime` is missing
        response = api_client.get(
            '/search/',
            {'enddate': '2015-08-12T12:10:12', 'site': 'lsc'})
        assert response.status_code == 400
        assert len(response.data) == 1
        assert response.data['datetime'][0] == 'This field is required.'

        # Wrong `site` value
        response = api_client.get(
            '/search/',
            {'datetime': '2015-08-12T12:10:12', 'site': 'xyz'})
        assert response.status_code == 400
        assert len(response.data) == 1
        assert response.data['site'][0] == '"xyz" is not a valid choice.'

        # With bad `aperture` parameter
        response = api_client.get(
            '/search/',
            {'datetime': '2015-08-12T12:10:12', 'site': 'lsc', 'aperture': 'abc'})
        assert response.status_code == 400
        assert len(response.data) == 1
        assert response.data['aperture'][0] == '"abc" is not a valid choice.'

        # With bad `callback` parameter
        response = api_client.get(
            '/search/',
            {'datetime': '2015-08-12T12:10:12', 'site': 'lsc', 'callback': 'xml'})
        assert response.status_code == 400
        assert response.data['callback'][0] == '"xml" is not a valid choice.'


    def test_api_v2(api_client):
        User.objects.create(username='somebody')  # we need a user because of the fixtures
        assert User.objects.filter(pk=1)

        call_command('loaddata', 'whatsup/fixtures/full_catalogue.json')
        response = api_client.get(
            '/search/v2/?start=2015-10-01T00:00:00&end=2015-10-01T12:00:00&aperture=1m0&full=true')
        assert response.status_code == 200
        targets = json.loads(response.content)['targets']
        assert len(targets) == 478

        # Checking all apertures in filter are `1m0`
        assert all([[f['aperture'] == '1m0' for f in target['filters']] for target in targets])
