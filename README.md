# Whats UP

Find what astronomical objects are visible above LCO sites from a curated list.

* [/whatsup](http://lco.global/whatsup) - Application address

## Returned values

Each call (from either endpoint) will return JSON response similar to below. `datetime` is the date and time the call was made.
```json
{
  "count": 113,
  "datetime": "2017-08-08T09:28:10",
  "targets":	[...],
	"site":"ogg",
}
```

The targets field (i.e. `[...]` above) will display to a list of multiple visible targets, in the format below.
```json
{
    "name": "NGC7479",
    "ra": 346.2361167,
    "dec": 12.3228778,
    "desc": "NGC 7479 (also known as Caldwell 44) is a barred spiral galaxy about 105 million light-years away in the constellation Pegasus. This is a beautiful barred spiral galaxy, seen almost face on.",
    "filters": [
        {
            "exposure": 240.0,
            "name": "rp"
        },
        {
            "exposure": 240.0,
            "name": "V"
        },
        {
            "exposure": 240.0,
            "name": "B"
        }
    ],
    "avmdesc": "Barred Galaxy",
    "avmcode": "5.3.2.2;5.1.2"
},
```

All suggested exposure times are scaled dependent on the `aperture` parameter and targets filtered to be appropriate to the field of view for the specified aperture.

## Endpoints

### Search

Accessed from [/whatsup/search/](https://lco.global/whatsup/search/). All visible objects are displayed.

#### Visibility
We calculate the visibility of targets in the Whats Up database by filtering only those targets which are within +/- 3.5 hours of the Local Sidereal Time at the specified `site` and `start`. We only display those targets greater than 30º above the horizon at `start`. Further filtering is performed using `aperture`, as the different field of views of LCO telescope classes can make some targets too large or small in images.

#### Parameters

The form/API expects the following querystring parameters:
* `start` - format must be `YYY-MM-DDTHH:MM:SS` in UTC,
* `site` - 3-letter site code for LCO sites. This can have the values `ogg`, `coj`, `elp`, `lsc`, or `cpt`.
* `aperture` - size of telescope. Can have values `2m0`, `1m0`, or `0m4`.
* `category` (optional) - filter by AVM category of target, e.g. `5.1.1` = Spiral Galaxies
* `format=jsonp` (optional) - for `jsonp` requests. Defaults to `json`

#### Example usage

Using required arguments only `start`, `aperture` and `site`:
```
https://lco.global/whatsup/search/?start=2017-08-08T09:28:10&aperture=0m4&site=ogg
```

A full example of all available arguments is:

```
https://lco.global/whatsup/search/?start=2017-08-08T09:28:10&aperture=1m0&site=ogg&category=5.1.1&format=jsonp
```

### Date Range

Accessed from [/whatsup/range/](https://lco.global/whatsup/range/). Provides a list of targets visible in northern and southern hemisphere during specified time range.

#### Visibility
We calculate the Right Ascension of the Sun at the midpoint between `start` and `end`. Targets in the Whats Up database are then filtering only those targets which are outside +/- 4 hours of the Sun's Right Ascension. Further filtering is performed using `aperture`, as the different field of views of LCO telescope classes can make some targets too large or small in images.

#### Parameters

The form/API expects the following querystring parameters:
* `start` - format must be `YYY-MM-DDTHH:MM:SS` in UTC,
* `end` - format must be `YYY-MM-DDTHH:MM:SS` in UTC,
* `aperture` - size of telescope. Can have values `2m0`, `1m0`, or `0m4`.
* `full=true/false` (optional) - Show full or truncated list of results. Defaults to `false` where a maximum of 30 random results are displayed.
* `category` (optional) - filter by AVM category of target, e.g. `5.1.1` = Spiral Galaxies
* `format=jsonp` (optional) - for `jsonp` requests. Defaults to `json`

#### Example usage

Using required arguments only `start`, `end` and `aperture`:
```
https://lco.global/whatsup/range/?start=2017-08-08T10:00:00&end=2017-08-17T10:00:00&aperture=0m4
```

A full example of all available arguments is:

```
https://lco.global/whatsup/range/?start=2017-08-08T10:00:00&end=2017-08-17T10:00:00&aperture=0m4&category=5.1.1&full=true&format=jsonp
```
