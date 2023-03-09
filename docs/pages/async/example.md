# Examples

Here, we'll have a look at implementation `geoserverx` asynchronous Class

!!! get "Get started"
    To start using `geoserverx` in Async mode, create a new instance of `AsyncGeoServerX` Class

## Setup Class instance

`AsyncGeoServerX` Class has default username, password, url which points to default geoserver settings. 
```Python
# Import class from package
from geoserverx._async.gsx import AsyncGeoServerX
import asyncio
# Create class Instance with default paramaters
client = AsyncGeoServerX()
```
We'll assume connection to local geoserver with default credentials

## Get all workspaces

```Python hl_lines="7"
from geoserverx._async.gsx import AsyncGeoServerX
import asyncio

async def get_info_raster_workspaces(url, username, password):
    print("-------------start-----------------")
    client = AsyncGeoServerX(username, password,url)
    print(await client.get_all_workspaces())

async def main():
    await asyncio.gather(get_info_raster_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver'),get_info_raster_workspaces(url='http://89.233.108.250:8080/geoserver/rest',username='admin', password='myP'),get_info_raster_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver'))

asyncio.run(main())

''' Console 
-------------start-----------------
-------------start-----------------
-------------start-----------------
workspaces=workspaceDict(workspace=[WorkspaceInBulk(name='MySimple', href='http://localhost:8080/geoserver/rest/workspaces/MySimple.json'), WorkspaceInBulk(name='MyHidden', href='http://localhost:8080/geoserver/rest/workspaces/MyHidden.json'), WorkspaceInBulk(name='MyDefault', href='http://localhost:8080/geoserver/rest/workspaces/MyDefault.json'), WorkspaceInBulk(name='nondefaultws', href='http://localhost:8080/geoserver/rest/workspaces/nondefaultws.json'), WorkspaceInBulk(name='mydefaultws', href='http://localhost:8080/geoserver/rest/workspaces/mydefaultws.json'), WorkspaceInBulk(name='ajadasfasdf', href='http://localhost:8080/geoserver/rest/workspaces/ajadasfasdf.json'), WorkspaceInBulk(name='ajada', href='http://localhost:8080/geoserver/rest/workspaces/ajada.json'), WorkspaceInBulk(name='aja', href='http://localhost:8080/geoserver/rest/workspaces/aja.json'), WorkspaceInBulk(name='cesium', href='http://localhost:8080/geoserver/rest/workspaces/cesium.json')])
'''
```

## Get Information about `cesium` workspace

```Python hl_lines="7"
from geoserverx._async.gsx import AsyncGeoServerX
import asyncio

async def get_info_raster_workspaces(url, username, password,workspace):
    print("-------------start-----------------")
    client = AsyncGeoServerX(username, password,url)
    print(await client.get_workspace(workspace))

async def main():
    await asyncio.gather(get_info_raster_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',workspace='cesium'))

asyncio.run(main())

''' Console 
-------------start-----------------
workspace=SingleWorkspace(name='cesium', isolated=False, dateCreated='2023-02-13 06:43:28.793 UTC', dataStores='http://localhost:8080/geoserver/rest/workspaces/cesium/datastores.json', coverageStores='http://localhost:8080/geoserver/rest/workspaces/cesium/coveragestores.json', wmsStores='http://localhost:8080/geoserver/rest/workspaces/cesium/wmsstores.json', wmtsStores='http://localhost:8080/geoserver/rest/workspaces/cesium/wmtsstores.json')
'''
```

## Create New workspaces

* MyDefault - Default and not Isolated
* MyHidden - Not Default and Isolated
* MySimple - Not Default and not Isolated

```Python hl_lines="7"
from geoserverx._async.gsx import AsyncGeoServerX
import asyncio

async def create_single_workspaces(url, username, password,workspace,default,isolated):
    print("-------------start-----------------")
    client = AsyncGeoServerX(username, password,url)
    print(await client.create_workspace(workspace, default,isolated))

async def main():
    await asyncio.gather(create_single_workspaces(
        url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='AsyncMyDefault',default=True,isolated= False),
create_single_workspaces(
        url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='AsyncMyHidden',default=False,isolated= True),
create_single_workspaces(
        url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='AsyncMySimple',default=False,isolated= False))

asyncio.run(main())

''' Console 
-------------start-----------------
-------------start-----------------
-------------start-----------------
code=201 response='Data added successfully'
code=201 response='Data added successfully'
code=201 response='Data added successfully'
'''
```

## Get all Vector stores in `cesium` workspace

```Python hl_lines="7"
from geoserverx._async.gsx import AsyncGeoServerX
import asyncio

async def create_single_workspaces(url, username, password,workspace):
    print("-------------start-----------------")
    client = AsyncGeoServerX(username, password,url)
    print(await client.get_vector_stores_in_workspaces(workspace))

async def main():
    await asyncio.gather(create_single_workspaces(
        url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='cesium'))

asyncio.run(main())

''' Console 
-------------start-----------------
dataStores=DataStoreDict(dataStore=[DataStoreInBulk(name='mygpkgs', href='http://localhost:8080/geoserver/rest/workspaces/cesium/datastores/mygpkgs.json'), DataStoreInBulk(name='myshp', href='http://localhost:8080/geoserver/rest/workspaces/cesium/datastores/myshp.json'), DataStoreInBulk(name='mysql', href='http://localhost:8080/geoserver/rest/workspaces/cesium/datastores/mysql.json')])
'''
```

## Get Information of Vector store `myshp` in `cesium` workspace

```Python hl_lines="7"
from geoserverx._async.gsx import AsyncGeoServerX
import asyncio

async def get_info_vector_workspaces(url, username, password,workspace,store):
    print("-------------start-----------------")
    client = AsyncGeoServerX(username, password,url)
    print(await client.get_vector_store(workspace,store))

async def main():
    await asyncio.gather(get_info_vector_workspaces(
        url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='cesium',store='myshp'))

asyncio.run(main())


''' Console 
-------------start-----------------
dataStore=DataStoreModelDetails(name='myshp', description=None, enabled=True, workspace=WorkspaceInBulk(name='cesium', href='http://localhost:8080/geoserver/rest/workspaces/cesium.json'), connectionParameters=EntryItem(entry=[DatastoreConnection(key='namespace', path='cesium'), DatastoreConnection(key='url', path='file:/path/to/nyc.shp')]), dateCreated='2023-02-28 18:14:01.199 UTC', dateModified=None, featureTypes='http://localhost:8080/geoserver/rest/workspaces/cesium/datastores/myshp/featuretypes.json')
'''
```
<!-- 
## Create new shapefile Vector store in `cesium` workspace with name `myshp`

Create new store using Shapefile available at given path
```Python hl_lines="8"
# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def add_vector_workspaces(url, username, password,workspace,store,file):
    print("-------------start-----------------")
    # Setup Class Instance
    client = SyncGeoServerX(username, password,url)
    return client.create_file_store(workspace, store, file, service_type='shapefile') 

result = add_vector_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='cesium',store='myshp', file='safe_users.zip' )
print(result.json())

''' Console 
-------------start-----------------
{"code": 201, "response": "Data added successfully"}
'''
```

![new_shp_vector](/../assets/images/new_shp_vector.png "new_shp_vector") -->

## Get all Raster stores in `cesium` workspace

```Python hl_lines="7"
from geoserverx._async.gsx import AsyncGeoServerX
import asyncio

async def get_all_raster_workspaces(url, username, password,workspace):
    print("-------------start-----------------")
    client = AsyncGeoServerX(username, password,url)
    print(await client.get_raster_stores_in_workspaces(workspace))

async def main():
    await asyncio.gather(get_all_raster_workspaces(
        url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',workspace='cesium'))

asyncio.run(main())

''' Console 
-------------start-----------------
coverageStores=CoveragesStoresDict(coverageStore=[CoveragesStoreInBulk(name='dem', href='http://localhost:8080/geoserver/rest/workspaces/cesium/coveragestores/dem.json'), CoveragesStoreInBulk(name='dsm', href='http://localhost:8080/geoserver/rest/workspaces/cesium/coveragestores/dsm.json'), CoveragesStoreInBulk(name='ortho', href='http://localhost:8080/geoserver/rest/workspaces/cesium/coveragestores/ortho.json')])
'''
```

## Get Information of Raster store `dsm` in `cesium` workspace

```Python hl_lines="7"
from geoserverx._async.gsx import AsyncGeoServerX
import asyncio

async def get_info_raster_workspaces(url, username, password,workspace,store):
    print("-------------start-----------------")
    client = AsyncGeoServerX(username, password,url)
    print(await client.get_raster_store(workspace,store))

async def main():
    await asyncio.gather(get_info_raster_workspaces(
        url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',workspace='cesium',store='dsm'))

asyncio.run(main())

''' Console 
-------------start-----------------
coverageStore=CoveragesStoreModelDetail(name='dsm', description=None, enabled=True, workspace=WorkspaceInBulk(name='cesium', href='http://localhost:8080/geoserver/rest/workspaces/cesium.json'), url='file:///Users/krishnaglodha/Desktop/IGI_DATA/DSM/IGI_DSM1m1.tif', coverages='http://localhost:8080/geoserver/rest/workspaces/cesium/coveragestores/dsm/coverages.json', dateCreated='2023-02-23 13:39:48.417 UTC', metadata=None)
'''
```

## Get all Styles in geoserver

```Python hl_lines="7"
from geoserverx._async.gsx import AsyncGeoServerX
import asyncio

async def get_info_raster_workspaces(url, username, password):
    print("-------------start-----------------")
    client = AsyncGeoServerX(username, password,url)
    print(await client.get_allstyles())

async def main():
    await asyncio.gather(get_info_raster_workspaces(
        url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver'))

asyncio.run(main())

''' Console 
-------------start-----------------
styles=allStyleDict(style=[allStyleList(name='burg', href='http://localhost:8080/geoserver/rest/styles/burg.json'), allStyleList(name='capitals', href='http://localhost:8080/geoserver/rest/styles/capitals.json'), allStyleList(name='cite_lakes', href='http://localhost:8080/geoserver/rest/styles/cite_lakes.json'), allStyleList(name='dem', href='http://localhost:8080/geoserver/rest/styles/dem.json'), allStyleList(name='generic', href='http://localhost:8080/geoserver/rest/styles/generic.json'), allStyleList(name='giant_polygon', href='http://localhost:8080/geoserver/rest/styles/giant_polygon.json'), allStyleList(name='grass', href='http://localhost:8080/geoserver/rest/styles/grass.json'), allStyleList(name='green', href='http://localhost:8080/geoserver/rest/styles/green.json'), allStyleList(name='line', href='http://localhost:8080/geoserver/rest/styles/line.json'), allStyleList(name='poi', href='http://localhost:8080/geoserver/rest/styles/poi.json'), allStyleList(name='point', href='http://localhost:8080/geoserver/rest/styles/point.json'), allStyleList(name='poly_landmarks', href='http://localhost:8080/geoserver/rest/styles/poly_landmarks.json'), allStyleList(name='polygon', href='http://localhost:8080/geoserver/rest/styles/polygon.json'), allStyleList(name='pophatch', href='http://localhost:8080/geoserver/rest/styles/pophatch.json'), allStyleList(name='population', href='http://localhost:8080/geoserver/rest/styles/population.json'), allStyleList(name='rain', href='http://localhost:8080/geoserver/rest/styles/rain.json'), allStyleList(name='raster', href='http://localhost:8080/geoserver/rest/styles/raster.json'), allStyleList(name='restricted', href='http://localhost:8080/geoserver/rest/styles/restricted.json'), allStyleList(name='simple_roads', href='http://localhost:8080/geoserver/rest/styles/simple_roads.json'), allStyleList(name='simple_streams', href='http://localhost:8080/geoserver/rest/styles/simple_streams.json'), allStyleList(name='tiger_roads', href='http://localhost:8080/geoserver/rest/styles/tiger_roads.json')])
'''
```

## Get Single Style in geoserver

```Python hl_lines="7"
from geoserverx._async.gsx import AsyncGeoServerX
import asyncio

async def get_info_raster_workspaces(url, username, password,style):
    print("-------------start-----------------")
    client = AsyncGeoServerX(username, password,url)
    print(await client.get_style(style))

async def main():
    await asyncio.gather(get_info_raster_workspaces(
        url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',style='poi'))

asyncio.run(main())
''' Console 
-------------start-----------------
style=SingleStyleDict(name='poi', format='sld', languageVersion=langVersion(version='1.0.0'), filename='poi.sld')
'''
```
