Whats UP
=======

Find what astronomical objects are visible above LCOGT sites from an curated list.

* [/whatsup](http://lcogt.net/whatsup) - Where the application is currently running. This is a very basic form because most interaction is via API

V1 Options
-------

Accessed from `/search/`.

The form/API expects the following querystring parameters:
* `start` - format must be `YYY-MM-DDTHH:MM:SS` in UTC,
* `site` - 3-letter site code for LCOGT sites. This can have the values `ogg`, `coj`, `elp`, `lsc`, or `cpt`.

Optional querystring parameters are:
* `end` - format must be `YYY-MM-DDTHH:MM:SS` in UTC,
* `name` - an astronomical object's catalogue name, e.g. M101,
* `aperture` - size of telescope. Can have values `2m0`, `1m0`, or `0m4`.
* `colour` - Not implemented yet. Will return 3 filters and appropriate exposure times.
* `format=jsonp` - for `jsonp` requests

V2 Options
-------

Accessed from `/search/v2/`.

The form/API expects the following querystring parameters:
* `start` - format must be `YYY-MM-DDTHH:MM:SS` in UTC,
* `site` - 3-letter site code for LCOGT sites. This can have the values `ogg`, `coj`, `elp`, `lsc`, or `cpt`.
* `aperture` - size of telescope. Can have values `2m0`, `1m0`, or `0m4`.

* Gives more than 1 filter response
* Aperture is now a mandatory parameter. Exposure times will be scaled dependent on this, and targets filtered to be appropriate to the available aperture.
