# Examples

Here, we'll have a look at implementation `geoserverx` synchronous Class

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
We'll assume connection to local geoserver with default credentials

## Get all workspaces

```Python hl_lines="8" linenums="1"
# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def get_all_gs_workspaces(url, username, password):
    print("-------------start-----------------")
    # Setup Class Instance 
    client = SyncGeoServerX(username, password,url)
    return client.get_all_workspaces()

result = get_all_gs_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver')
print(result.json())
''' Console 
-------------start-----------------
{"workspaces": {"workspace": [{"name": "nondefaultws", "href": "http://localhost:8080/geoserver/rest/workspaces/nondefaultws.json"}, 
{"name": "mydefaultws", "href": "http://localhost:8080/geoserver/rest/workspaces/mydefaultws.json"}, 
{"name": "ajadasfasdf", "href": "http://localhost:8080/geoserver/rest/workspaces/ajadasfasdf.json"}, 
{"name": "ajada", "href": "http://localhost:8080/geoserver/rest/workspaces/ajada.json"}, 
{"name": "aja", "href": "http://localhost:8080/geoserver/rest/workspaces/aja.json"}, {"name": "cesium", "href": "http://localhost:8080/geoserver/rest/workspaces/cesium.json"}]}}
'''
```

## Get Information about `cesium` workspace

```Python hl_lines="7"
# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def get_single_workspaces(url, username, password,workspace):
    print("-------------start-----------------")
    # Setup Class Instance
    client = SyncGeoServerX(username, password,url)
    return client.get_workspace(workspace)

result = get_single_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',workspace='cesium')

print(result.json())
''' Console 
-------------start-----------------
{"workspace": {"name": "cesium", "isolated": false, "dateCreated": "2023-02-13 06:43:28.793 UTC", "dataStores": "http://localhost:8080/geoserver/rest/workspaces/cesium/datastores.json", "coverageStores": "http://localhost:8080/geoserver/rest/workspaces/cesium/coveragestores.json", "wmsStores": "http://localhost:8080/geoserver/rest/workspaces/cesium/wmsstores.json", "wmtsStores": "http://localhost:8080/geoserver/rest/workspaces/cesium/wmtsstores.json"}}
'''
```

## Create New workspaces

* MyDefault - Default and not Isolated
* MyHidden - Not Default and Isolated
* MySimple - Not Default and not Isolated

```Python hl_lines="11 12 14 15 17 18"

# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX


def create_single_workspaces(url, username, password,workspace,default,isolated):
    print("-------------start-----------------")
    # Setup Class Instance
    client = SyncGeoServerX(username, password,url)
    return client.create_workspace(workspace, default,isolated)

first = create_single_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='MyDefault',default=True,isolated= False)
print(first.json())
second = create_single_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='MyHidden',default=False,isolated= True)
print(second.json())
third = create_single_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='MySimple',default=False,isolated= False)
print(third.json())
''' Console 
-------------start-----------------
-------------start-----------------
-------------start-----------------
code=201 response='Data added successfully'
code=201 response='Data added successfully'
code=201 response='Data added successfully'
'''
```
![workspace created](/assets/images/workspace_created.png "workspace created")

## Get all Vector stores in `cesium` workspace

```Python hl_lines="8"

# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def get_all_vector_workspaces(url, username, password,workspace):
    print("-------------start-----------------")
    # Setup Class Instance
    client = SyncGeoServerX(username, password,url)
    return client.get_vector_stores_in_workspaces(workspace)

result = get_vector_store(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='cesium')
print(result.json())

''' Console 
-------------start-----------------
{"dataStores": {"dataStore": [{"name": "mysqlllllll", "href": "http://localhost:8080/geoserver/rest/workspaces/cesium/datastores/mysqlllllll.json"}]}}
'''
```

## Get Information of Vector store `mysqldb` in `cesium` workspace

```Python hl_lines="8"

# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def get_info_vector_workspaces(url, username, password,workspace,store):
    print("-------------start-----------------")
    # Setup Class Instance
    client = SyncGeoServerX(username, password,url)
    return client.get_vector_store(workspace,store)

result = get_info_vector_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='cesium',store='mysqldb' )
print(result.json())

''' Console 
-------------start-----------------
{"dataStore": {"name": "mysqldb", "description": null, "enabled": true, 
"workspace": {"name": "cesium", "href": "http://localhost:8080/geoserver/rest/workspaces/cesium.json"}, 
"connectionParameters": {"entry": [{"key": "Evictor run periodicity", "path": "300"}, {"key": "fetch size", "path": "1000"}, {"key": "Expose primary keys", "path": "false"}, {"key": "validate connections", "path": "true"}, {"key": "Connection timeout", "path": "20"}, {"key": "Batch insert size", "path": "1"}, {"key": "database", "path": "appsolicitous_dcra"}, {"key": "port", "path": "3306"}, {"key": "passwd", "path": "crypt1:jxnPgWTsBoUAVin1wtCLWgIqmZ4DSEWx"}, {"key": "storage engine", "path": "MyISAM"}, {"key": "min connections", "path": "1"}, {"key": "dbtype", "path": "mysql"}, {"key": "host", "path": "23.29.118.44"}, {"key": "namespace", "path": "cesium"}, {"key": "max connections", "path": "10"}, {"key": "Evictor tests per run", "path": "3"}, {"key": "Test while idle", "path": "true"}, {"key": "user", "path": "appsolicitous_dcra"}, {"key": "Max connection idle time", "path": "300"}]}, "dateCreated": "2023-02-28 10:38:52.70 UTC", "dateModified": null, 
"featureTypes": "http://localhost:8080/geoserver/rest/workspaces/cesium/datastores/mysqlllllll/featuretypes.json"}}
'''
```

## Create new shapefile Vector store in `cesium` workspace with name `natural_earth`

Create new store using Shapefile available at given path
```Python hl_lines="8"
from geoserverx._sync.gsx import SyncGeoServerX

def add_vector_workspaces(url, username, password,workspace,store,file):
    print("-------------start-----------------")
    # Setup Class Instance
    client = SyncGeoServerX(username, password,url)
    return client.create_file_store(workspace, store, file, service_type='shapefile') 

result = add_vector_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='cesium',store='natural_earth', file='/Users/krishnaglodha/Downloads/ne_10m_populated_places_simple/ne_10m_populated_places_simple.shp' )
print(result.json())
''' Console 
-------------start-----------------
{"code": 201, "response": "Data added successfully"}
'''
```

![new_shp_vector](/assets/images/new_shp_vector.png "new_shp_vector")

## Get all Raster stores in `cesium` workspace

```Python hl_lines="8"
# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def get_all_raster_workspaces(url, username, password,workspace):
    print("-------------start-----------------")
    # Setup Class Instance
    client = SyncGeoServerX(username, password,url)
    return client.get_raster_stores_in_workspaces(workspace)

result = get_all_raster_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='cesium')
print(result.json())

''' Console 
-------------start-----------------
{"coverageStores": {"coverageStore": [{"name": "dem", "href": "http://localhost:8080/geoserver/rest/workspaces/cesium/coveragestores/dem.json"}, {"name": "dsm", "href": "http://localhost:8080/geoserver/rest/workspaces/cesium/coveragestores/dsm.json"}, {"name": "ortho", "href": "http://localhost:8080/geoserver/rest/workspaces/cesium/coveragestores/ortho.json"}]}}
'''
```

## Get Information of Raster store `dsm` in `cesium` workspace

```Python hl_lines="8"
# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def get_info_raster_workspaces(url, username, password,workspace,store):
    print("-------------start-----------------")
    # Setup Class Instance
    client = SyncGeoServerX(username, password,url)
    return client.get_raster_store(workspace,store)

result = get_info_raster_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='cesium',store='dsm' )
print(result.json())

''' Console 
-------------start-----------------
{"coverageStore": {"name": "dsm", "description": null, "enabled": true, "workspace": {"name": "cesium", "href": "http://localhost:8080/geoserver/rest/workspaces/cesium.json"}, "url": "file:///Users/krishnaglodha/Desktop/IGI_DATA/DSM/IGI_DSM1m1.tif", "coverages": "http://localhost:8080/geoserver/rest/workspaces/cesium/coveragestores/dsm/coverages.json", "dateCreated": "2023-02-23 13:39:48.417 UTC", "metadata": null}}
'''
```

## Get all Styles in geoserver

```Python hl_lines="8"
# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def get_all_styles(url, username, password):
    print("-------------start-----------------")

    client = SyncGeoServerX(username, password,url)
    return client.get_allstyles()

result = get_all_styles(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver' )
print(result.json())

''' Console 
-------------start-----------------
{"styles": {"style": [{"name": "burg", "href": "http://localhost:8080/geoserver/rest/styles/burg.json"}, {"name": "capitals", "href": "http://localhost:8080/geoserver/rest/styles/capitals.json"}, {"name": "cite_lakes", "href": "http://localhost:8080/geoserver/rest/styles/cite_lakes.json"}, {"name": "dem", "href": "http://localhost:8080/geoserver/rest/styles/dem.json"}, {"name": "generic", "href": "http://localhost:8080/geoserver/rest/styles/generic.json"}, {"name": "giant_polygon", "href": "http://localhost:8080/geoserver/rest/styles/giant_polygon.json"}, {"name": "grass", "href": "http://localhost:8080/geoserver/rest/styles/grass.json"}, {"name": "green", "href": "http://localhost:8080/geoserver/rest/styles/green.json"}, {"name": "line", "href": "http://localhost:8080/geoserver/rest/styles/line.json"}, {"name": "poi", "href": "http://localhost:8080/geoserver/rest/styles/poi.json"}, {"name": "point", "href": "http://localhost:8080/geoserver/rest/styles/point.json"}, {"name": "poly_landmarks", "href": "http://localhost:8080/geoserver/rest/styles/poly_landmarks.json"}, {"name": "polygon", "href": "http://localhost:8080/geoserver/rest/styles/polygon.json"}, {"name": "pophatch", "href": "http://localhost:8080/geoserver/rest/styles/pophatch.json"}, {"name": "population", "href": "http://localhost:8080/geoserver/rest/styles/population.json"}, {"name": "rain", "href": "http://localhost:8080/geoserver/rest/styles/rain.json"}, {"name": "raster", "href": "http://localhost:8080/geoserver/rest/styles/raster.json"}, {"name": "restricted", "href": "http://localhost:8080/geoserver/rest/styles/restricted.json"}, {"name": "simple_roads", "href": "http://localhost:8080/geoserver/rest/styles/simple_roads.json"}, {"name": "simple_streams", "href": "http://localhost:8080/geoserver/rest/styles/simple_streams.json"}, {"name": "tiger_roads", "href": "http://localhost:8080/geoserver/rest/styles/tiger_roads.json"}]}}
'''
```

## Get Single Style in geoserver

```Python hl_lines="8"
# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def get_style_info(url, username, password,style):
    print("-------------start-----------------")

    client = SyncGeoServerX(username, password,url)
    return client.get_style(style)

result = get_style_info(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',style='poi' )
print(result.json())
''' Console 
-------------start-----------------
{"style": {"name": "poi", "format": "sld", "languageVersion": {"version": "1.0.0"}, "filename": "poi.sld"}}
'''
```
