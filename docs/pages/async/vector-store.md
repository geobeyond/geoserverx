# Vector Stores 

`geoserverx` allows users to access all/one vector stores from geoserver. As of now, `geoserverx` also supports new vector store creation for `shapefile` and `gpkg` data

!!! get "Get started"
    To start using `geoserverx` in Sync mode, create a new instance of `SyncGeoServerX` Class

## Setup Class instance

<div class="termy">
```py
from geoserverx._sync.gsx import SyncGeoServerX
client = SyncGeoServerX(username='admin', password='geoserver',url='127.0.0.1')
```
</div>

## Get all Vector stores 

<div class="termy">
```py
client.get_vector_stores_in_workspaces('cite')
```
</div>


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