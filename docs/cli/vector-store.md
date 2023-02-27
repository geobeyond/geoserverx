# Vector Stores 

`geoserverx` allows users to access all/one vector stores from geoserver. As of now, `geoserverx` also supports new vector store creation for `shapefile` and `gpkg` data

!!! get "Get started"
    To start using `geoserverx` in Sync mode, create a new instance of `SyncGeoServerX` Class

## Setup Class instance

```py
from geoserverx._sync.gsx import SyncGeoServerX
client = SyncGeoServerX(username='admin', password='geoserver',url='127.0.0.1')
```

## Get all Vector stores 

```py
client.get_vector_stores_in_workspaces('cite')
```


## Get single Vector store

```py
client.get_vector_store(workspace='cite', store='shape') 
```


## Create new shapefile Vector store

```py
client.create_file_store(workspace='cite', store='shape', file='path/for/shapefile', service_type='shapefile') 
```

## Create new geopackage Vector store

```py
client.create_file_store(workspace='cite', store='shape', file='path/for/gpkg', service_type='gpkg') 
```