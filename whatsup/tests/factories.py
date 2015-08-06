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
