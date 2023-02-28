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
    # Get all workspaces
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

```Python hl_lines="8"
# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def get_single_workspaces(url, username, password,workspace):
    print("-------------start-----------------")
    # Get single workspaces
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


def get_single_workspaces(url, username, password,workspace,default,isolated):
    print("-------------start-----------------")
    # Get single workspaces
    client = SyncGeoServerX(username, password,url)
    return client.create_workspace(workspace, default,isolated)

first = get_single_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='MyDefault',default=True,isolated= False)
print(first.json())
second = get_single_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='MyHidden',default=False,isolated= True)
print(second.json())
third = get_single_workspaces(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver',
workspace='MySimple',default=False,isolated= False)
print(third.json())
''' Console 
-------------start-----------------
{"code": 201, "response": "Data added successfully"}
-------------start-----------------
{"code": 201, "response": "Data added successfully"}
-------------start-----------------
{"code": 201, "response": "Data added successfully"}
'''
```
![workspace created](/../assets/images/workspace_created.png "workspace created")



## Get all Vector datasets in `cesium` workspace

```Python hl_lines="8"

# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def get_all_vector_workspaces(url, username, password,workspace):
    print("-------------start-----------------")
    # Get single workspaces
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

## Get Information Vector dataset `mysqldb` in `cesium` workspace

```Python hl_lines="8"

# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX

def get_info_vector_workspaces(url, username, password,workspace,store):
    print("-------------start-----------------")
    # Get single workspaces
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


## Create new shapefile Vector store in `cesium` workspace with name `myshp`

Create new store using Shapefile available at given path
```Python
# Import Class from Package
from geoserverx._sync.gsx import SyncGeoServerX


def add_vector_workspaces(url, username, password,workspace,store,file):
    print("-------------start-----------------")
    # Get single workspaces
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

![new_shp_vector](/../assets/images/new_shp_vector.png "new_shp_vector")