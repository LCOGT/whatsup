from datetime import datetime

from astropy import units as u
from astropy.coordinates import earth_orientation as earth
from astropy.time import Time
from django.conf import settings
from django.db.models import Q
from numpy import sin, cos, arcsin, arccos, pi, arctan2, radians, degrees, floor

from .models import Target

coords = settings.COORDS

def eqtohorizon(hour, dec, lat):
    """
    Convert hour angle, declination of an astronomical source and the latitude of the observer to azimuth and
    altitude (in degs)
    """
    dec_rad = dec * pi / 180.
    lat_rad = lat * pi / 180.
    h_rad = hour * pi / 12.
    sin_alt = sin(dec_rad) * sin(lat_rad) + cos(dec_rad) * cos(lat_rad) * cos(h_rad)
    alt_rad = arcsin(sin_alt)
    cos_az = (sin(dec_rad) - sin(lat_rad) * sin_alt) / (cos(lat_rad) * cos(alt_rad))
    return arccos(cos_az) * 180. / pi, alt_rad * 180. / pi


def calc_lst(start, site):
    """
    Calculate local siderial time at a given location and at a specific date/time
    """
    t1 = Time(start, scale='utc')
    mjd = t1.jd - 2451545.000
    tel_long_deg = coords[site]['lon']
    UT = t1.datetime.hour + t1.datetime.minute/60. + t1.datetime.second/3600.
    n, lst_deg = divmod(100.46 + 0.985647 * mjd + tel_long_deg + 15.*UT, 360.)
    lst_hours = lst_deg/15.
    return lst_hours


def ra_sun(start):
    # days since 1 Jan 2010 Epoch
    t = Time(start, scale='utc')
    d = (start - datetime(2010, 1, 1)).days
    eg = 279.557208  # ecliptic longitude at epoch 2010
    wg = 283.112438  # ecliptic longitude of perigee at epoch 2010
    e = 0.016705  # eccentricity at 2010 epoch
    N = (360. / 365.242191) * d % 360
    m_sun = N + eg + wg
    if m_sun < 0:
        m_sun += 360.
    Ec = (360. / pi) * e * sin(radians(m_sun))
    l_sun = N + Ec + eg
    obliquity = earth.obliquity(t.jd, algorithm=1980)
    y = sin(radians(l_sun)) * cos(radians(obliquity))
    x = cos(radians(l_sun))
    ra = degrees(arctan2(y, x)) / 15
    return ra
