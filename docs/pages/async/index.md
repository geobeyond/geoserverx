# Asynchronous way of using geoserverx

`geoserverx` allows user to call methods asynchronously.

!!! get "Get started"
To start using `geoserverx` in Sync mode, create a new instance of `AsyncGeoServerX` Class

## Setup Class instance

`AsyncGeoServerX` Class has default username, password, url which points to default GeoServer settings.

```Python
# Import class from package
from geoserverx._async.gsx import AsyncGeoServerX
# Create class Instance with default paramaters
client = AsyncGeoServerX()
```

These paramaters however can be changed as follows

This class can also be used as context manager to manage the opening and closing connection automatically.
