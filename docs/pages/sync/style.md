# Style 

`geoserverx` allows users to access all/one styles from geoserver.

!!! get "Get started"
    To start using `geoserverx` in Sync mode, create a new instance of `SyncGeoServerX` Class

## Setup Class instance

<div class="termy">
```py
from geoserverx._sync.gsx import SyncGeoServerX
client = SyncGeoServerX(username='admin', password='geoserver',url='127.0.0.1')
```
</div>

## Get all Styles  

<div class="termy">
```py
client.get_allstyles()
```
</div>

## Get single Style

<div class="termy">
```py
client.get_style('population') 
```
</div>