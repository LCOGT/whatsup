# Whats UP

Find what astronomical objects are visible above LCO sites from a curated list.

* [/whatsup](http://lco.global/whatsup) - Where the application is currently running. This is a very basic form because most interaction is via API

## Endpoints

### Search

Accessed from `/search/`. Provides a list of targets visible in northern and southern hemisphere during time range

The form/API expects the following querystring parameters:
* `start` - format must be `YYY-MM-DDTHH:MM:SS` in UTC,
* `site` - 3-letter site code for LCO sites. This can have the values `ogg`, `coj`, `elp`, `lsc`, or `cpt`.
* `aperture` - size of telescope. Can have values `2m0`, `1m0`, or `0m4`.
* `full=true/false` (optional) - Show full or truncated list of results,
* `category` (optional) - filter by AVM category of target, e.g. `5.1.1` = Spiral Galaxies
* `format=jsonp` (optional) - for `jsonp` requests

* Exposure times are scaled dependent on the aperture and targets filtered to be appropriate to the available aperture.

### Date Range

Accessed from `/range/`. Provides a list of targets visible in northern and southern hemisphere during time range

The form/API expects the following querystring parameters:
* `start` - format must be `YYY-MM-DDTHH:MM:SS` in UTC,
* `end` - format must be `YYY-MM-DDTHH:MM:SS` in UTC,
* `aperture` - size of telescope. Can have values `2m0`, `1m0`, or `0m4`.
* `full=true/false` (optional) - Show full or truncated list of results,
* `category` (optional) - filter by AVM category of target, e.g. `5.1.1` = Spiral Galaxies
* `format=jsonp` (optional) - for `jsonp` requests
