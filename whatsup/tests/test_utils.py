import datetime

from ..views import find_target, targets_not_behind_sun, eqtohorizon, calc_lst, visible_targets, UTtoGST, ra_sun


def test_UTtoGST():
    dt = datetime.datetime.now()
    assert UTtoGST(dt)


def test_eqtohorizon():
    assert eqtohorizon(3, 12, 23)


def test_ra_sun():
    dt = datetime.datetime.now()
    assert ra_sun(dt)