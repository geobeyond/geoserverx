# Workspaces 

`geoserverx` allows users to access all/one workspace from geoserver, along with ability to add new workspaces. 

To start using `geoserverx` in Sync mode, create a new instance of `SyncGeoServerX` Class

## Setup Class instance

```py
from geoserverx._sync.gsx import SyncGeoServerX
client = SyncGeoServerX(username, password,url)

```

```bash echo 'Hello world' ```

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
- Name `str` : To define Name of the workspace
- default `bool` : To define whether to keep workspace as default or not
- Isolated `bool` : To define whether to keep workspace Isolated or not

```py
client.create_workspace(name='my_wrkspc',default=True,Isolated=True)
```
