# Workspaces 

`geoserverx` allows users to access all/one workspace from GeoServer, along with ability to add new workspaces. 

## Get all workspaces
This command fetches all workspaces available in GeoServer. No parameters are required to be passed.

```py
# Get all workspaces in GeoServer
await client.get_all_workspaces()
```

## Get single workspace
This command fetches workspace with paramter as name of it from GeoServer.
```Python
# Get workspace with name `cite`
await client.get_workspace('cite')
```

## Create workspace
This command allows user to create new workspace. 
Creating new workspace requires following parameters

* Name `str` : To define Name of the workspace
* default `bool` : To define whether to keep workspace as default or not
* Isolated `bool` : To define whether to keep workspace Isolated or not
  
```Python
#Create new workspace with name `my_wrkspc` , make it Default and Isolated
await client.create_workspace(name='my_wrkspc',default=True,Isolated=True)
```
