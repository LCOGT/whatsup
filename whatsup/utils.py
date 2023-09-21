import random
from datetime import datetime

from astroplan import Observer, FixedTarget
from astroplan import (AirmassConstraint, AtNightConstraint)
from astroplan import is_observable
from astropy import units as u
from astropy.coordinates import earth_orientation as earth
from astropy.coordinates import SkyCoord, EarthLocation
from astropy.time import Time
from django.conf import settings
from django.db.models import Q, Prefetch
import numpy as np

from .models import Target, Params

coords = settings.COORDS

constraints = [AirmassConstraint(2), AtNightConstraint.twilight_civil()]

def eqtohorizon(hour, dec, lat):
    """
    Convert hour angle, declination of an astronomical source and the latitude of the observer to azimuth and
    altitude (in degs)
    """
    dec_rad = dec * np.pi / 180.
    lat_rad = lat * np.pi / 180.
    h_rad = hour * np.pi / 12.
    sin_alt = np.sin(dec_rad) * np.sin(lat_rad) + np.cos(dec_rad) * np.cos(lat_rad) * np.cos(h_rad)
    alt_rad = np.arcsin(sin_alt)
    cos_az = (np.sin(dec_rad) - np.sin(lat_rad) * sin_alt) / (np.cos(lat_rad) * np.cos(alt_rad))
    return np.arccos(cos_az) * 180. / np.pi, alt_rad * 180. / np.pi

def calc_lst(start, site):
    """
    Calculate local siderial time at a given location and at a specific date/time
    """
    t1 = Time(start, scale='utc')
    mjd = t1.jd - 2451545.000
    tel_long_deg = coords[site]['lon']
    UT = t1.datetime.hour + t1.datetime.minute/60. + t1.datetime.second/3600.
    n, lst_deg = np.divmod(100.46 + 0.985647 * mjd + tel_long_deg + 15.*UT, 360.)
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
    Ec = (360. / np.pi) * e * np.sin(np.radians(m_sun))
    l_sun = N + Ec + eg
    obliquity = earth.obliquity(t.jd, algorithm=1980)
    y = np.sin(np.radians(l_sun)) * np.cos(np.radians(obliquity))
    x = np.cos(np.radians(l_sun))
    ra = np.degrees(np.arctan2(y, x)) / 15
    return ra

def visible_targets(start, end=None, site=None, category=None, mode=None):
    s1 = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
    targets = Target.objects.all()

    if mode == 'messier':
        targets = targets.filter(name__startswith='M')
    elif mode == 'best':
        targets = targets.filter(best=True)
    if category:
        join_cat = ";{}".format(category)
        targets = targets.filter(Q(avm_code__startswith=category) | Q(avm_code__contains=join_cat))
    if end:
        # Option for range
        e1 = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        time_range = Time([s1, e1], format='datetime')
    else:
        times = Time([s1], format='datetime')
    if not site:
        sites = coords.keys()
    else:
        if "," in site:
            sites = site.split(",")
        else:
            sites = [site]

    targetid_list = []
    for site in sites:
        elevation = coords[site]['alt'] * u.m
        location = EarthLocation.from_geodetic(coords[site]['lon'], coords[site]['lat'], elevation)
        observer = Observer(location=location, name=site, timezone='UTC')
        targetlist = [FixedTarget(coord=SkyCoord(ra=t.ra*u.deg, dec=t.dec*u.deg), name=t.name) for t in targets]
        targetids = [t.id for t in targets]
        if end:
            # Option for range
            ever_observable = is_observable(constraints, observer, targetlist, time_range=time_range, time_grid_resolution=2*u.hour)
        else:
            ever_observable = is_observable(constraints, observer, targetlist, times=times, time_grid_resolution=2*u.hour)
        target_array = np.array(targetids)
        targetid_list += list(target_array[ever_observable])
        
    return set(targetid_list)

def _visible_targets(start, site, aperture=None, category=None, mode=None):
    """
    Produce a list of targets which visible to observer at specified date/time
    """
    # start=  "2014-07-21T14:00:00"
    # Find which targets are in the correct RA range, i.e. LST +/-3.5hours
    lst = calc_lst(start, site)
    lst_deg = (lst * u.hourangle).to(u.deg)/u.deg
    dha = (3.5*u.hourangle).to(u.deg)/u.deg
    s0 = lst_deg - dha if (lst_deg - dha) > 0. else lst_deg - dha + 360.
    e0 = lst_deg + dha if (lst_deg + dha) < 360. else lst_deg + dha - 360.
    if s0 < 360. and e0 < s0 :
        tgs = Target.objects.filter(Q(ra__gte=float(s0)) | Q(ra__lte=float(e0)), ~Q(avm_desc='')).order_by('avm_desc')
    else:
        tgs = Target.objects.filter(~Q(avm_desc=''), ra__gte=float(s0), ra__lte=float(e0)).order_by('avm_desc')
    if category:
        join_cat = ";{}".format(category)
        tgs = tgs.filter(Q(avm_code__startswith=category) | Q(avm_code__contains=join_cat))
    targets = []
    # # Filter these targets by which are above (horizon + 30deg) for observer
    for t in list(tgs):
        hour = lst - float((t.ra * u.deg).to(u.hourangle) / u.hourangle)
        az, alt = eqtohorizon(hour, t.dec, coords[site]['lat'])
        if alt >= 30.:
            targets.append(t)
    return targets

def search_targets(query_params):
    if not query_params:
        return []
    site = query_params.get('site', '')
    start = query_params.get('start', '')
    category = query_params.get('category', '')
    aperture = query_params.get('aperture', None)
    mode = query_params.get('mode', None)
    targets = visible_targets(start=start, site=site, category=category, mode=mode)
    targets = Target.objects.filter(id__in=targets)
    if aperture:
        return filter_targets_with_aperture(targets, aperture, mode)
    return targets

def range_targets(query_params):
    if not query_params:
        return []
    start = query_params.get('start', '')
    end = query_params.get('end', '')
    mode = query_params.get('mode', '')
    category = query_params.get('category', '')
    s1 = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
    e1 = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
    aperture = query_params.get('aperture', None)
    # Find targets within a date range (i.e. not behind Sun during that time)
    targets = visible_targets(start=start, end=end, category=category, mode=mode)
    if mode == 'best':
        targets = random.choices(list(targets), k=5)
    elif mode != 'full':
        targets = random.choices(list(targets), k=30)
    targets = Target.objects.filter(id__in=targets)
    if aperture:
        return filter_targets_with_aperture(targets, aperture, mode)
    return targets

def find_target(name):
    t = Target.objects.filter(name__icontains=name)
    if t.count() > 0:
        resp = {
            'name': t[0].name,
            'ra': t[0].ra,
            'dec': t[0].dec,
            'exp': t[0].exposure,
            'desc': t[0].description,
            'avmdesc': t[0].avm_desc,
            'avmcode': t[0].avm_code
        }
    else:
        resp = "'error' : 'Target not found.'"
    return resp


def targets_not_behind_sun(start):
    ra = ra_sun(start)
    start = (ra - 4.) % 24
    end = (ra + 4.) % 24
    tgs = Target.objects.exclude(ra__gte=start, ra__lte=end)
    return tgs


def targets_all(aperture='0m4', category=None):
    tgs = Target.objects.filter(~Q(avm_desc='')).order_by('avm_desc')
    if aperture:
        tgs = filter_targets_with_aperture(tgs, aperture)
    if category:
        join_cat = ";{}".format(category)
        tgs = tgs.filter(Q(avm_code__startswith=category) | Q(avm_code__contains=join_cat))
    return tgs



def filter_targets_with_aperture(targets, aperture, mode=None):
    """
    Filter queryset, prefetch related params while filtering them agains aperture parameter
    :param targets: Target queryset
    :param aperture: aperture parameter
    :return: queryset
    """
    prefetch = Prefetch('parameters', queryset=Params.objects.filter(aperture=aperture))
    if mode == 'rti':
        return targets.filter(parameters__aperture=aperture, parameters__exposure__lte=600.).prefetch_related(prefetch).distinct()
    else:
        return targets.filter(parameters__aperture=aperture).prefetch_related(prefetch).distinct()
