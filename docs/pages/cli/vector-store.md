# Vector Stores 

`geoserverx` allows users to access all/one vector stores from geoserver. As of now, `geoserverx` also supports new vector store creation for `shapefile` and `gpkg` data

!!! get "Get started"
    To start using `geoserverx` using command line, activate the Environment where package is installed and use `gsx` command


## Get all Vector stores in workspace

<div class="termy">

```
 gsx vector-st-wp --help
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


As listed above, `vector-st-wp` command accepts four parameters. 

* request type ( sync or async )
* url - Geoserver REST URL
* password - Password for geoserver
* username - Username for geoserver

All these parameters have default value setup which will work for local default installation

## Get single Vector store

<div class="termy">
```py
client.get_vector_store(workspace='cite', store='shape') 
```
</div>

## Create new shapefile Vector store

<div class="termy">
```py
client.create_file_store(workspace='cite', store='shape', file='path/for/shapefile', service_type='shapefile') 
```
</div>

## Create new geopackage Vector store

<div class="termy">
```py
client.create_file_store(workspace='cite', store='shape', file='path/for/gpkg', service_type='gpkg') 
```
</div>