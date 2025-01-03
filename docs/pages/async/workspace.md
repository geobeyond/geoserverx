# Workspaces

`geoserverx` allows users to access all/one workspace from GeoServer, along with ability to do CRUD operations on workspaces.

!!! get "Get started"
To start using `geoserverx` in Sync mode, create a new instance of `AsyncGeoServerX` Class, read more about it [here](https://geobeyond.github.io/geoserverx/pages/async/)

## Get all workspaces

This command fetches all workspaces available in GeoServer. No parameters are required to be passed.

```py

```

## Get single workspace

Fetches workspace details.

```Python
# Get workspace with name `cite`
await client.get_workspace('cite')
```

## Create workspace

This command allows user to create new workspace.
Creating new workspace requires following parameters

| Parameter | Required                      | Default value | Data type | Description                                            |
| --------- | ----------------------------- | ------------- | --------- | ------------------------------------------------------ |
| Name      | :white_check_mark:            |               | `str`     | To define Name of the workspace                        |
| default   | :negative_squared_cross_mark: | `False`       | `bool`    | To define whether to keep workspace as default or not  |
| isolated  | :negative_squared_cross_mark: | `False`       | `bool`    | To define whether to keep workspace as Isolated or not |

```Python
#Create new workspace with name `my_wrkspc` , make it Default and Isolated
await client.create_workspace(name='my_wrkspc',default=True,Isolated=True)
```

## Delete workspace

This command allows user to delete workspace.

| Parameter | Required                      | Default value | Data type | Description                                                                                                                                           |
| --------- | ----------------------------- | ------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| workspace | :white_check_mark:            |               | `str`     | Name of the workspace                                                                                                                                 |
| recurse   | :negative_squared_cross_mark: | `False`       | `bool`    | This parameter recursively deletes all layers referenced by the specified workspace, including data stores, coverage stores, feature types, and so on |

```Python

```

## Update workspace

This command allows user to update existing workspace.
Updating workspace requires following parameters

| Parameter | Required           | Data type                                                                                                                                             | Description                          |
| --------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| name      | :white_check_mark: | `str`                                                                                                                                                 | Name of the workspace to be updated  |
| update    | :white_check_mark: | [`UpdateWorkspaceInfo`](https://github.com/geobeyond/geoserverx/blob/b7757c9f0130864b06c40c2faa17afc841fc705f/src/geoserverx/models/workspace.py#L42) | To define body of the update request |

```Python
#Updating workspace with name `my_wrkspc` , make is Isolated and rename it to `my_new_wrkspc`
from geoserverx.models.workspace import UpdateWorkspaceInfo

await client.update_workspace(name='my_wrkspc',update=UpdateWorkspaceInfo(name='my_new_wrkspc',isolated=True))
```
