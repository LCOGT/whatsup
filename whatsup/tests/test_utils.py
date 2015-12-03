import datetime

from ..views import find_target, targets_not_behind_sun, eqtohorizon, calc_lst, visible_targets, ra_sun


def test_eqtohorizon():
    assert eqtohorizon(3, 12, 23)


def test_ra_sun():
    dt = datetime.datetime.now()
    assert ra_sun(dt)

def test_calc_lst():
    dt = datetime.datetime(2015,12,3,14,0,0)
    site = 'ogg'
    lst_hours = calc_lst(dt,site)
    assert lst_hours > 8.35 and lst_hours < 8.4
