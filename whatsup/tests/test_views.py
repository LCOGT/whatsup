import pytest

from django.core.management import call_command

from ..models import Target

pytestmark = pytest.mark.django_db  # Explicit db access authorization


def test_homepage_should_respond(client):
    response = client.get('/')
    assert response.status_code == 200


def test_search_page__should_respond(client):
    response = client.get('/search/')
    assert response.status_code == 200


def test_search_page__form(client):
    response = client.get('/search/json/', {'datetime': '2015-06-13T00:22:00', 'site': 'ogg'})
    assert response.status_code == 200


