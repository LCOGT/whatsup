import pytest

from django.core.management import call_command

from ..models import Target

pytestmark = pytest.mark.django_db  # Explicit db access authorization


def test_management_command_ingest_guidedtours():
    call_command('loaddata', 'whatsup/fixtures/full_catalogue.json')
    c = Target.objects.all()
    assert c.count() == 433
