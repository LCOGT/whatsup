import pytest

from django.core.management import call_command
from django.contrib.auth import get_user_model
from ..models import Target

pytestmark = pytest.mark.django_db  # Explicit db access authorization


def test_management_command_load_full_catalogue():
    # We need an existing user with a `pk` equal to 1 to load current fixtures
    User = get_user_model()
    if not User.objects.filter(pk=1).exists():
        User.objects.create(username='who')
    call_command('loaddata', 'whatsup/fixtures/full_catalogue.json')
    c = Target.objects.all()
    assert c.count() == 478
