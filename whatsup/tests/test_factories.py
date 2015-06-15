import pytest

from .factories import ConstellationFactory, ProjectFactory, TargetFactory

pytestmark = pytest.mark.django_db


def test_it_should_create_a_constellation():
    constellation = ConstellationFactory()
    assert constellation.pk is not None
    assert unicode(constellation)


def test_it_should_create_a_project():
    project = ProjectFactory()
    assert project.pk is not None
    assert unicode(project)


def test_it_should_create_a_target():
    target = TargetFactory()
    assert target.pk is not None
    assert unicode(target)