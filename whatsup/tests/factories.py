import factory

from ..models import Constellation, Project, Target


class ConstellationFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Constellation name %s" % n)
    shortname = factory.Sequence(lambda n: "AB %s" % (n % 9))

    class Meta:
        model = Constellation


class ProjectFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Project name %s" % n)
    shortname = factory.Sequence(lambda n: "Proj  %s" % n)

    class Meta:
        model = Project


class TargetFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Target name %s" % n)

    class Meta:
        model = Target