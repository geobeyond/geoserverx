# Workspaces 

`geoserverx` allows users to access all/one workspace from geoserver, along with ability to add new workspaces. 

!!! get "Get started"
    To start using `geoserverx` in Sync mode, create a new instance of `AsyncGeoServerX` Class


## Setup Class instance

<div class="termy">

```console
from geoserverx._async.gsx import AsyncGeoServerX
client = AsyncGeoServerX(username='admin', password='geoserver',url='127.0.0.1')
```
</div>

## Get all workspaces

<div class="termy">

```py
client.get_all_workspaces()
```
</div>

## Get single workspace

<div class="termy">
```py
client.get_workspace('cite')
```
</div>

## Create workspace

Creating new workspace requires following parameters

* Name `str` : To define Name of the workspace
* default `bool` : To define whether to keep workspace as default or not
* Isolated `bool` : To define whether to keep workspace Isolated or not
  
<div class="termy">
```py
client.create_workspace(name='my_wrkspc',default=True,Isolated=True)
```
</div>