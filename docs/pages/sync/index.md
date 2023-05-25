# Synchronous way of using geoserverx

`geoserverx` allows user to call methods synchronously. 

!!! get "Get started"
    To start using `geoserverx` in Sync mode, create a new instance of `SyncGeoServerX` Class

## Setup Class instance

`SyncGeoServerX` Class has default username, password, url which points to default geoserver settings. 
```Python
# Import class from package
from geoserverx._sync.gsx import SyncGeoServerX 
# Create class Instance with default paramaters
client = SyncGeoServerX()
```

These paramaters however can be changed as follows
```Python
# Import class from package
from geoserverx._sync.gsx import SyncGeoServerX
# Create class Instance with custom paramaters
client = SyncGeoServerX(username='mygeos', password='SecuredPass',url='http://127.0.0.1:9090/geoserver/rest/')
```

This class can also be used as context manager to manage the opening and closing connection automatically.
```Python
# Import class from package
from geoserverx._sync.gsx import SyncGeoServerX
# Create class Instance with custom paramaters
client = SyncGeoServerX(username='mygeos', password='SecuredPass',url='http://127.0.0.1:9090/geoserver/rest/')

#Using with as 
with client as cl :
    response = cl.get_all_workspaces()
```