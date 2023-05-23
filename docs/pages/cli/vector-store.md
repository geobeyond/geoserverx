# Vector Stores 

`geoserverx` allows users to access all/one vector stores from geoserver. As of now, `geoserverx` also supports new vector store creation for `shapefile` and `gpkg` data

!!! get "Get started"
    To start using `geoserverx` using command line, activate the Environment where package is installed and use `gsx` command


## Paramters for all Vector stores in Workspace command

<div class="termy">
```console
$ gsx vector-st-wp --help
Usage: gsx vector-st-wp [OPTIONS]

  Get vector stores in specific workspaces
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

As listed above, `vector-st-wp` command accepts following parameters. 

* request type ( sync or async )
* url - Geoserver REST URL
* password - Password for geoserver
* username - Username for geoserver

All these parameters have default value setup which will work for local default installation. Apart from this `workspace` paramters must be added which aims at the workspace we are interested in

##  Get all Vector stores

<div class="termy">
```console
$ gsx vector-st-wp --workspace cesium
{"dataStores": {"dataStore": [{"name": "mysqlllllll", "href": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/datastores/mysqlllllll.json"}]}}
```
</div>

## Paramters for single Vector stores command

<div class="termy">
```console
$ gsx vector-store --help
Usage: gsx vector-store [OPTIONS]

  Get vector store information in specific workspaces

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
