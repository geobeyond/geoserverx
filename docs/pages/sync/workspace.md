# Workspaces 

`geoserverx` allows users to access all/one workspace from GeoServer, along with ability to do CRUD operations on workspaces. 

!!! get "Get started"
    To start using `geoserverx` in Sync mode, create a new instance of `SyncGeoServerX` Class, ream more about it [here](https://geobeyond.github.io/geoserverx/pages/sync/)


## Get all workspaces
This command fetches all workspaces available in GeoServer. No paramters are required to be passed.

```Python
# Get all workspaces in GeoServer
client.get_all_workspaces()
```

## Get single workspace
This command fetches workspace with paramter as name of it from GeoServer.
```Python
# Get workspace with name `cite`
client.get_workspace('cite')
```

## Create workspace
This command allows user to create new workspace. 
Creating new workspace requires following parameters

* Name `str` : To define Name of the workspace
* default `bool` : To define whether to keep workspace as default or not
* Isolated `bool` : To define whether to keep workspace Isolated or not
  
```Python
#Create new workspace with name `my_wrkspc` , make it Default and Isolated
client.create_workspace(name='my_wrkspc',default=True,Isolated=True)
```

## Delete workspace
This command allows user to delete  workspace. 
Deleting workspace requires following parameters

* workspace `str` : Name of the workspace

```Python
#Delete workspace with name `my_wrkspc`.
client.delete_workspace(workspace='my_wrkspc')
```

## Update workspace
This command allows user to update existing workspace. 
Updating workspace requires following parameters

* name `str` : To define Name of the workspace
* update `UpdateWorkspaceInfo` : To define body of the update request
  
```Python
#Updating workspace with name `my_wrkspc` , make is Isolated and rename it to `my_new_wrkspc`
from geoserverx.models.workspace import UpdateWorkspaceInfo

client.update_workspace(name='my_wrkspc',update=UpdateWorkspaceInfo(name='my_new_wrkspc',isolated=True))
```