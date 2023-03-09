# Raster Stores 

`geoserverx` allows users to access all/one raster stores from geoserver. As of now, `geoserverx` also supports new raster store creation for `shapefile` and `gpkg` data

!!! get "Get started"
    To start using `geoserverx` using command line, activate the Environment where package is installed and use `gsx` command


## Paramters for all raster stores in Workspace command

<div class="termy">
```console
$ gsx raster-st-wp --help
Usage: gsx raster-st-wp [OPTIONS]

  Get raster stores in specific workspaces

Options:
  --request [sync|async]  [default: requestEnum._sync]
  --workspace TEXT        Workspace name  [required]
  --url TEXT              Geoserver REST URL  [default:
                          http://127.0.0.1:8080/geoserver/rest/]
  --password TEXT         Geoserver Password  [default: geoserver]
  --username TEXT         Geoserver username  [default: admin]
  --help                  Show this message and exit.
```
</div>

As listed above, `raster-st-wp` command accepts following parameters. 

* request type ( sync or async )
* url - Geoserver REST URL
* password - Password for geoserver
* username - Username for geoserver

All these parameters have default value setup which will work for local default installation. Apart from this `workspace` paramters must be added which aims at the workspace we are interested in

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

## Paramters for single raster stores command

<div class="termy">
```console
$ gsx raster-store --help
Usage: gsx raster-store [OPTIONS]

  Get raster store information in specific workspaces

Options:
  --request [sync|async]  [default: requestEnum._sync]
  --workspace TEXT        Workspace name  [required]
  --store TEXT            Store name  [required]
  --url TEXT              Geoserver REST URL  [default:
                          http://127.0.0.1:8080/geoserver/rest/]
  --password TEXT         Geoserver Password  [default: geoserver]
  --username TEXT         Geoserver username  [default: admin]
  --help                  Show this message and exit.

```
</div>

This command takes an additional parameter of name of the store.

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
