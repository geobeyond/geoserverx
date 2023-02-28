# Style

`geoserverx` allows users to access all/one raster stores from geoserver. As of now, `geoserverx` also supports new raster store creation for `shapefile` and `gpkg` data

!!! get "Get started"
    To start using `geoserverx` using command line, activate the Environment where package is installed and use `gsx` command


## Paramters for all styles command

<div class="termy">
```console
$ gsx styles --help
Usage: gsx styles [OPTIONS]

  Get all styles in Geoserver

Options:
  --request [sync|async]  [default: requestEnum._sync]
  --url TEXT              Geoserver REST URL  [default:
                          http://127.0.0.1:8080/geoserver/rest/]
  --password TEXT         Geoserver Password  [default: geoserver]
  --username TEXT         Geoserver username  [default: admin]
  --help                  Show this message and exit.
```
</div>

As listed above, `styles` command accepts following parameters. 

* request type ( sync or async )
* url - Geoserver REST URL
* password - Password for geoserver
* username - Username for geoserver

All these parameters have default value setup which will work for local default installation. 

##  Get all styles

<div class="termy">
```console
$ gsx styles       
{"styles": {"style": [{"name": "burg", "href": 
"http://127.0.0.1:8080/geoserver/rest/styles/burg.json"}, {"name": "capitals", "href": 
"http://127.0.0.1:8080/geoserver/rest/styles/capitals.json"}, {"name": "cite_lakes", 
"href": "http://127.0.0.1:8080/geoserver/rest/styles/cite_lakes.json"}, {"name": "dem", 
"href": "http://127.0.0.1:8080/geoserver/rest/styles/dem.json"}, {"name": "generic", 
"href": "http://127.0.0.1:8080/geoserver/rest/styles/generic.json"}, {"name": 
"giant_polygon", "href": 
"http://127.0.0.1:8080/geoserver/rest/styles/giant_polygon.json"}, {"name": "grass", 
"href": "http://127.0.0.1:8080/geoserver/rest/styles/grass.json"}, {"name": "green", 
"href": "http://127.0.0.1:8080/geoserver/rest/styles/green.json"}, {"name": "line", 
"href": "http://127.0.0.1:8080/geoserver/rest/styles/line.json"}]}}
```
</div>

## Paramters for single style command

<div class="termy">
```console
$ gsx style --help 
Usage: gsx style [OPTIONS]

  Get style in Geoserver

Options:
  --request [sync|async]  [default: requestEnum._sync]
  --url TEXT              Geoserver REST URL  [default:
                          http://127.0.0.1:8080/geoserver/rest/]
  --style TEXT            Style name  [required]
  --password TEXT         Geoserver Password  [default: geoserver]
  --username TEXT         Geoserver username  [default: admin]
  --help                  Show this message and exit.

```
</div>

This command takes an additional parameter of name of the style.

##  Get single style information

<div class="termy">
```console
$ gsx style --style p
oi
{"style": {"name": "poi", "format": "sld", "languageVersion": {"version": "1.0.0"}, 
"filename": "poi.sld"}}
```
</div>

