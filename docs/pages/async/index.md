# Asynchronous way of using geoserverx

`geoserverx` allows user to call methods asynchronously. 

!!! get "Get started"
    To start using `geoserverx` in Sync mode, create a new instance of `AsyncGeoServerX` Class

## Setup Class instance

`AsyncGeoServerX` Class has default username, password, url which points to default geoserver settings. 
```Python
# Import class from package
from geoserverx._async.gsx import AsyncGeoServerX 
# Create class Instance with default paramaters
client = AsyncGeoServerX()
```

These paramaters however can be changed as follows
```Python
# Import class from package
from geoserverx._async.gsx import AsyncGeoServerX
# Create class Instance with custom paramaters
client = AsyncGeoServerX(username='mygeos', password='SecuredPass',url='http://127.0.0.1:9090/geoserver/rest/')
```


This class can also be used as context manager to manage the opening and closing connection automatically.
```Python
# Import class from package
from geoserverx._async.gsx import  AsyncGeoServerX,GeoServerXAuth
import asyncio
# Create class Instance with custom paramaters
client = AsyncGeoServerX(username='mygeos', password='SecuredPass',url='http://127.0.0.1:9090/geoserver/rest/')

#Using with as 
async def main():
        async with client as cl:
                response = await cl.get_all_workspaces()
                print(response)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```