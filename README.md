Whats UP
=======

Find what astronomical objects are visible above LCOGT sites from an curated list.

* [/whatsup](http://lcogt.net/whatsup) - Where the application is currently running. This is a very basic form because most interaction is via API

Options
-------

The form/API expects the following querystring parameters:
* `datetime` - format must be `YYY-MM-DDTHH:MM:SS` in UTC,
* `site` - 3-letter site code for LCOGT sites. This can have the values `ogg`, `coj`, `elp`, `lsc`, or `cpt`.

Optional querystring parameters are:
* `enddate` - format must be `YYY-MM-DDTHH:MM:SS` in UTC,
* `name` - an astronomical object's catalogue name, e.g. M101,
* `aperture` - size of telescope. Can have values `2m0`, `1m0`, or `0m4`.
* `colour` - Not implemented yet. Will return 3 filters and appropriate exposure times.
* `callback` - for `jsonp` requests

