# Workspaces 

`geoserverx` allows users to access all/one workspace from geoserver, along with ability to add new workspaces. 

## Get all workspaces
This command fetches all workspaces available in geoserver. No paramters are required to be passed.

```Python
# Get all workspaces in geoserver
client.get_all_workspaces()
```

## Get single workspace
This command fetches workspace with paramter as name of it from geoserver.
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
