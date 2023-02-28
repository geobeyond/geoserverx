# Raster Stores 

`geoserverx` allows users to access all/one raster stores from geoserver

!!! get "Get started"
    To start using `geoserverx` in Sync mode, create a new instance of `SyncGeoServerX` Class

## Setup Class instance

<div class="termy">
```py
from geoserverx._sync.gsx import SyncGeoServerX
client = SyncGeoServerX(username='admin', password='geoserver',url='127.0.0.1')
```
</div>

## Get all raster stores 

<div class="termy">
```py
client.get_raster_stores_in_workspaces('cite')
```
</div>

## Get single raster store

<div class="termy">
```py
client.get_raster_store(workspace='cite', store='image') 
```
</div>