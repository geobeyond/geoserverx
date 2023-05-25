# Examples

Here, we'll have a look at implementation `geoserverx` synchronous Class.

!!! get "Get started"
    To start using `gsx` CLI tool, install `geoserverx` package and turn on the environment.

## Setup CLI instance

<div class="termy">
```console
$ pip install geoserverx
---> 100%

$  gsx
Usage: gsx [OPTIONS] COMMAND [ARGS]...
Try 'gsx --help' for help.

Error: Missing command.
```
</div>

We'll assume connection to local geoserver with default credentials 


## Get all workspaces

<div class="termy">
```console
$ gsx workspaces

{"workspaces": {"workspace": [{"name": "cesium", "href": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium.json"}]}}
```
</div>


## Get single workspaces

<div class="termy">
```console
$ gsx workspace --workspace cesium
{"workspace": {"name": "cesium", "isolated": false, "dateCreated": "2023-02-13 
06:43:28.793 UTC", "dataStores": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/datastores.json", 
"coverageStores": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/coveragestores.json", 
"wmsStores": "http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/wmsstores.json", 
"wmtsStores": "http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/wmtsstores.json"}}
```
</div>


## Create single workspaces

<div class="termy">
```console
$ gsx create-workspace --workspace mydefaultws --default
code=201 response='Data added successfully'
```
</div>

##  Get all Vector stores

<div class="termy">
```console
$ gsx vector-st-wp --workspace cesium
{"dataStores": {"dataStore": [{"name": "mysqlllllll", "href": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/datastores/mysqlllllll.json"}]}}
```
</div>


##  Get single Vector store information

<div class="termy">
```console
$ gsx vector-store --workspace cesium --store mysqlllllll
{"dataStore": {"name": "mysqlllllll", "description": null, "enabled": true, "workspace": 
{"name": "cesium", "href": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium.json"}, "connectionParameters": 
{"entry": [{"key": "Evictor run periodicity", "path": "300"}, {"key": "fetch size", 
"path": "1000"}, {"key": "Expose primary keys", "path": "false"}, {"key": "validate 
connections", "path": "true"}, {"key": "Connection timeout", "path": "20"}, {"key": 
"Batch insert size", "path": "1"}, {"key": "database", "path": "appsolicitous_dcra"}, 
{"key": "port", "path": "3306"}, {"key": "passwd", "path": 
"crypt1:njsGJk9CEY8jiaqfSYyQGZeB9RLB2sh7"}, {"key": "storage engine", "path": "MyISAM"}, 
{"key": "min connections", "path": "1"}, {"key": "dbtype", "path": "mysql"}, {"key": 
"host", "path": "23.29.118.44"}, {"key": "namespace", "path": "cesium"}, {"key": "max 
connections", "path": "10"}, {"key": "Evictor tests per run", "path": "3"}, {"key": "Test
while idle", "path": "true"}, {"key": "user", "path": "appsolicitous_dcra"}, {"key": "Max
connection idle time", "path": "300"}]}, "dateCreated": "2023-02-28 10:38:52.70 UTC", 
"dateModified": null, "featureTypes": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/datastores/mysqlllllll/featuretyp
es.json"}}

```
</div>


##  Get all raster stores

<div class="termy">
```console
$ gsx raster-st-wp --workspace cesium
{"coverageStores": {"coverageStore": [{"name": "dem", "href": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/coveragestores/dem.json"}, 
{"name": "dsm", "href": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/coveragestores/dsm.json"}, 
{"name": "ortho", "href": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/coveragestores/ortho.json"}]}}
```
</div>


##  Get single raster store information

<div class="termy">
```console
$ gsx raster-store --workspace cesium --store dsm
{"coverageStore": {"name": "dsm", "description": null, "enabled": true, "workspace": 
{"name": "cesium", "href": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium.json"}, "url": 
"file:///Users/krishnaglodha/Desktop/IGI_DATA/DSM/IGI_DSM1m1.tif", "coverages": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/coveragestores/dsm/coverages.json
", "dateCreated": "2023-02-23 13:39:48.417 UTC", "metadata": null}}

```
</div>


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

##  Get single style information

<div class="termy">
```console
$ gsx style --style p
oi
{"style": {"name": "poi", "format": "sld", "languageVersion": {"version": "1.0.0"}, 
"filename": "poi.sld"}}
```
</div>

