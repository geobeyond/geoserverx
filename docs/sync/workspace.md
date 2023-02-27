# Workspaces 

`geoserverx` allows users to access all/one workspace from geoserver, along with ability to add new workspaces. 

!!! get "Get started"
    To start using `geoserverx` in Sync mode, create a new instance of `SyncGeoServerX` Class


## Setup Class instance

<div class="termy">
```py
from geoserverx._sync.gsx import SyncGeoServerX
client = SyncGeoServerX(username='admin', password='geoserver',url='127.0.0.1')
```
</div>


## Get all workspaces

```py
client.get_all_workspaces()
```


## Get single workspace

```py
client.get_workspace('cite')
```

## Create workspace

Creating new workspace requires following parameters

* Name `str` : To define Name of the workspace
* default `bool` : To define whether to keep workspace as default or not
* Isolated `bool` : To define whether to keep workspace Isolated or not

```py
client.create_workspace(name='my_wrkspc',default=True,Isolated=True)
```
