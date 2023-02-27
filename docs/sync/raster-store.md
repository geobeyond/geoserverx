# Raster Stores 

`geoserverx` allows users to access all/one raster stores from geoserver

!!! get "Get started"
    To start using `geoserverx` in Sync mode, create a new instance of `SyncGeoServerX` Class

## Setup Class instance

```py
from geoserverx._sync.gsx import SyncGeoServerX
client = SyncGeoServerX(username='admin', password='geoserver',url='127.0.0.1')
```

## Get all raster stores 

```py
client.get_raster_stores_in_workspaces('cite')
```


## Get single raster store

```py
client.get_raster_store(workspace='cite', store='image') 
```