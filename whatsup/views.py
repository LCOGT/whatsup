from django.http import HttpResponse, Http404
from django.shortcuts import render
import json
from numpy import sin, cos,arcsin, arccos, pi
from astropy.time import Time
from astropy import units as u
import time

from whatsup.models import *

coords = {
        'ogg': {'lat':20.7075, 'lon': -156.256111},
        'coj': {'lat':-31.273333, 'lon': 149.071111},
        'lsc': {'lat':-30.1675, 'lon': -70.804722},
        'elp': {'lat':30.67, 'lon': -104.02},
        'sqa': {'lat':20.7075, 'lon': -156.256111},
        'cpt': {'lat':-32.38, 'lon':  20.81},
        }

def home(request):
    return render(request, 'home.html', {})

def search(request,format=None):
    error = None
    info = ''
    site = request.GET.get('site','')
    start = request.GET.get('datetime','')
    try:
        time.strptime(start, "%Y-%m-%dT%H:%M:%S") 
    except:
        error = "Date/time format must be YYYY-MM-DDTHH:MM:SS"
    try:
        coords[site]
    except:
        error = "Site provided is not official LCOGT site abbreviation. i.e. ogg, coj, cpt, lsc or elp"
    callback = request.GET.get('callback','')
    if not error:
        targets = visible_targets(start,site)
        info = { 'site' : site,
                 'datetime' : start,
                 'targets'  : targets,
                }
        if format == 'json':
            resp = json.dumps(info,indent=2)
            if callback:
                resp = "%s([%s])" % (callback,resp)
            return HttpResponse(resp, content_type="application/json")
        else:
            return render(request, 'whatsup/home.html', {"data": info})
    else:
        if format == 'json':
            resp = "'error':'%s'" % error
            if callback:
                resp = "%s([%s])" % (callback,resp)
            return HttpResponse(resp, content_type="application/json")
        else:
            return render(request, 'home.html', {'data': info,'error':error})

def visible_targets(start,site):
    '''
    Produce a list of targets which visible to observer at specified date/time
    '''
    # start=  "2014-07-21T14:00:00"
    # Find which targets are in the correct RA range, i.e. LST +/-2hours
    lst = calc_lst(start,site)
    s0 =float(((lst-2.)*u.hourangle).to(u.degree)/u.deg)
    e0 =float(((lst+2.)*u.hourangle).to(u.degree)/u.deg)
    tgs = Target.objects.filter(ra__gte=s0,ra__lte=e0).order_by('avm_desc')
    targets = []
    # Filter these targets by which are above (horizon + 30deg) for observer
    for t in tgs:
        hour = lst - float((t.ra*u.deg).to(u.hourangle)/u.hourangle)
        az,alt = eqtohorizon(hour,t.dec,coords[site]['lat'])
        if alt >= 30.:
            params = { 'name'   : t.name,
                       'ra'     : t.ra,
                       'dec'    : t.dec,
                       'exp'    : t.exposure,
                       'desc'   : t.description,
                       'avmdesc': t.avm_desc}
            targets.append(params)    
    return targets

def UTtoGST(start):
    '''
    Convert UT to Greenwich Siderial Time
    '''
    t1= Time(start,scale='utc')
    s = t1.jd - 2451545.000
    t = s/36525.000
    t0 = 6.697374558 + (2400.051336*t) + (0.000025862*(t*t))
    t0 = (t0 - int(t0/24.)*24)
    if t0 < 0.0: t0 = t0 + 24.
    ut = 1.002737909*t1.datetime.hour
    tmp = int((ut + t0)/24.)
    gst = ut + t0 - tmp*24.
    gst_hour = int(gst)
    gst_min  = int((gst - gst_hour)*60.)
    gst_sec  = int((gst - gst_hour - gst_min/60.)*3600.)
    #print "%2.2d %2.2d %2.2d" % (gst_hour, gst_min, gst_sec)
    return gst

def eqtohorizon(hour,dec,lat):
    '''
    Convert hour angle, declination of an astronomical source and the latitude of the observer to azimuth and altitude (in degs)
    '''
    dec_rad = dec*pi/180.
    lat_rad = lat*pi/180.
    h_rad = hour*pi/180.
    sin_alt = sin(dec_rad)*sin(lat_rad) + cos(dec_rad)*cos(lat_rad)*cos(h_rad)
    alt_rad = arcsin(sin_alt)
    cos_az = (sin(dec_rad) - sin(lat_rad)*sin_alt)/(cos(lat_rad)*cos(alt_rad))
    return arccos(cos_az)*180./pi, alt_rad*180./pi

# def eqtoaltaz():
#     gatech = ephem.Observer()
#     gatech.lon = '-156.256111'
#     gatech.lat = '20.7075'
#     gatech.elevation = 320
#     gatech.date = '2014/7/22 08:22:56'
#     polaris = ephem.readdb("Polaris,f|M|F7,2:31:48.704,89:15:50.72,2.02,2000")
#     polaris.compute(gatech)
#     print polaris.alt, polaris.az
#     return polaris.alt, polaris.az

def calc_lst(start,site):
    '''
    Calculate local siderial time at a given location and at a specific date/time
    '''
    tel_long_deg = coords[site]['lon']
    sid = UTtoGST(start) 
    lst_hours = sid + tel_long_deg/15.
    lst_hours = lst_hours % 24.
    lst_hr  = int(lst_hours)
    lst_min = int((lst_hours - lst_hr)*60.)
    lst_sec = int((lst_hours - lst_hr - lst_min/60.)*3600.)
    #print "%2.2d %2.2d %2.2d" % (lst_hr, lst_min, lst_sec)
    return lst_hours




