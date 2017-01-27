import datetime
from django.conf import settings
from astropy import units as u

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

def test_alt_calc_coj():
    # Check altitude of eta Car from coj
    dt = datetime.datetime(2017, 1, 27, 12, 9, 15, 350624)
    site = 'coj'
    lst = calc_lst(dt,site)
    dec = -59.6844306
    ra = 161.264775
    hour = lst - float((ra * u.deg).to(u.hourangle) / u.hourangle)
    assert hour == -4.19467577246047
    az, alt = eqtohorizon(hour, dec, settings.COORDS[site]['lat'])
    assert az == 143.99819724394061
    assert alt == 40.130620483063822

def test_alt_calc_ogg():
    # Check altitude of target from OGG
    dt = datetime.datetime(2017, 1, 27, 12, 9, 15, 350624)
    site = 'ogg'
    lst = calc_lst(dt,site)
    ra = 185.9353958
    dec = 12.47835
    hour = lst - float((ra * u.deg).to(u.hourangle) / u.hourangle)
    assert hour == -2.1945319591271293
    az, alt = eqtohorizon(hour, dec, settings.COORDS[site]['lat'])
    assert az == 99.385588357342769
    assert alt == 57.465994710651884
