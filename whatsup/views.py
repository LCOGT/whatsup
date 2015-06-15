"""
WhatsUP: astronomical object suggestions for Las Cumbres Observatory Global Telescope Network
Copyright (C) 2014-2015 LCOGT

views.py - data wrangling for templates

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from datetime import datetime
import json
import random

from astropy.coordinates import earth_orientation as earth
from astropy.time import Time
from astropy import units as u
from numpy import sin, cos, arcsin, arccos, pi, arctan2, radians, degrees

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from whatsup.models import *

coords = {
    'ogg': {'lat': 20.7075, 'lon': -156.256111},
    'coj': {'lat': -31.273333, 'lon': 149.071111},
    'lsc': {'lat': -30.1675, 'lon': -70.804722},
    'elp': {'lat': 30.67, 'lon': -104.02},
    'sqa': {'lat': 20.7075, 'lon': -156.256111},
    'cpt': {'lat': -32.38, 'lon': 20.81},
    'tfn': {'lat': 28.3, 'lon': -16.51},
}


def home(request):
    return render(request, 'home.html', {})


def search(request, formatting=None):
    error = None
    info = ''
    site = request.GET.get('site', '')
    start = request.GET.get('datetime', '')
    end = request.GET.get('enddate', '')
    callback = request.GET.get('callback', '')
    full = request.GET.get('full', '')
    e1 = None
    s1 = None
    name = request.GET.get('name', '')
    aperture = request.GET.get('aperture', None)
    if request.GET.get('colour'):
        colour = True
    else:
        colour = True
    if name:
        info = find_target(name)
        resp = json.dumps(info, indent=2)
        if callback:
            resp = "%s([%s])" % (callback, resp)
        return HttpResponse(resp, content_type="application/json")

    try:
        s1 = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        error = "Date/time format must be YYYY-MM-DDTHH:MM:SS"
    if start and end:
        try:
            e1 = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            error = "End date/time format must be YYYY-MM-DDTHH:MM:SS"
    else:
        try:
            coords[site]
        except KeyError:
            error = "Site provided is not official LCOGT site abbreviation. i.e. ogg, coj, cpt, lsc or elp"
    if not error:
        if s1 and e1:
            # Find targets within a date range (i.e. not behind Sun during that time)
            meandate = s1 + (e1 - s1) / 2
            targets = targets_not_behind_sun(meandate, aperture)
            if full != 'true':
                targets = random.sample(targets, 30)
        else:
            # Find targets for only date/time given
            targets = visible_targets(start, site, aperture, colour)
        # Package all targets and confirmation of date/time and site selected
        info = {'site': site,
                'datetime': start,
                'targets': targets, }
        if formatting == 'json':
            resp = json.dumps(info, indent=2)
            if callback:
                resp = "%s([%s])" % (callback, resp)
            return HttpResponse(resp, content_type="application/json")
        else:
            return render(request, 'whatsup/home.html', {"data": info})
    else:
        if formatting == 'json':
            resp = "'error':'%s'" % error
            if callback:
                resp = "%s([%s])" % (callback, resp)
            return HttpResponse(resp, content_type="application/json")
        else:
            return render(request, 'home.html', {'data': info, 'error': error})


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


def targets_not_behind_sun(start, aperture=None, colour=True):
    targets = []
    ra = ra_sun(start)
    start = (ra - 4.) % 24
    end = (ra + 4.) % 24
    tgs = Target.objects.exclude(avm_desc='', ra__gte=start, ra__lte=end)
    if aperture:
        tgs = tgs.filter(aperture=aperture)
    for t in tgs:
        params = {'name': t.name,
                  'ra': t.ra,
                  'dec': t.dec,
                  'exp': t.exposure,
                  'desc': t.description,
                  'avmdesc': t.avm_desc, }
        if colour:
            params['filters'] = t.filters.split(',')[0]
        else:
            params['filters'] = t.filters
        targets.append(params)
    return targets


def visible_targets(start, site, name=None, aperture=None, colour=True):
    """
    Produce a list of targets which visible to observer at specified date/time
    """
    # start=  "2014-07-21T14:00:00"
    # Find which targets are in the correct RA range, i.e. LST +/-2hours
    lst = calc_lst(start, site)
    s0 = float(((lst - 2.) * u.hourangle).to(u.degree) / u.deg)
    e0 = float(((lst + 2.) * u.hourangle).to(u.degree) / u.deg)
    tgs = Target.objects.filter(~Q(avm_desc=''), ra__gte=s0, ra__lte=e0).order_by('avm_desc')
    if aperture:
        tgs = tgs.filter(aperture=aperture)
    targets = []
    # Filter these targets by which are above (horizon + 30deg) for observer
    for t in tgs:
        hour = lst - float((t.ra * u.deg).to(u.hourangle) / u.hourangle)
        az, alt = eqtohorizon(hour, t.dec, coords[site]['lat'])
        if alt >= 30.:
            params = {'name': t.name,
                      'ra': t.ra,
                      'dec': t.dec,
                      'exp': t.exposure,
                      'desc': t.description,
                      'avmdesc': t.avm_desc,
                      'alt': alt,
                      'az': az, }
            targets.append(params)
            if colour:
                params['filters'] = t.filters.split(',')[0]
            else:
                params['filters'] = t.filters
    targets = sorted(targets, key=lambda k: k['alt'])
    targets.reverse()
    return targets


def UTtoGST(start):
    """
    Convert UT to Greenwich Siderial Time
    """
    t1 = Time(start, scale='utc')
    s = t1.jd - 2451545.000
    t = s / 36525.000
    t0 = 6.697374558 + (2400.051336 * t) + (0.000025862 * (t * t))
    t0 = (t0 - int(t0 / 24.) * 24)
    if t0 < 0.0:
        t0 += 24.
    ut = 1.002737909 * t1.datetime.hour
    tmp = int((ut + t0) / 24.)
    gst = ut + t0 - tmp * 24.
    gst_hour = int(gst)
    gst_min = int((gst - gst_hour) * 60.)
    gst_sec = int((gst - gst_hour - gst_min / 60.) * 3600.)
    return gst


def eqtohorizon(hour, dec, lat):
    """
    Convert hour angle, declination of an astronomical source and the latitude of the observer to azimuth and altitude (in degs)
    """
    dec_rad = dec * pi / 180.
    lat_rad = lat * pi / 180.
    h_rad = hour * pi / 180.
    sin_alt = sin(dec_rad) * sin(lat_rad) + cos(dec_rad) * cos(lat_rad) * cos(h_rad)
    alt_rad = arcsin(sin_alt)
    cos_az = (sin(dec_rad) - sin(lat_rad) * sin_alt) / (cos(lat_rad) * cos(alt_rad))
    return arccos(cos_az) * 180. / pi, alt_rad * 180. / pi


def calc_lst(start, site):
    """
    Calculate local siderial time at a given location and at a specific date/time
    """
    tel_long_deg = coords[site]['lon']
    sid = UTtoGST(start)
    lst_hours = sid + tel_long_deg / 15.
    lst_hours = lst_hours % 24.
    lst_hr = int(lst_hours)
    lst_min = int((lst_hours - lst_hr) * 60.)
    lst_sec = int((lst_hours - lst_hr - lst_min / 60.) * 3600.)
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



