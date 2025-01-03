# Workspaces

`geoserverx` allows users to access all/one workspace from GeoServer, along with ability to do CRUD operations on workspaces.

!!! get "Get started"
To start using `geoserverx` , initiate new Class as stated [here](/geoserverx/pages/docs/)

## Get all workspaces

This command fetches all workspaces available in GeoServer. No paramters are required to be passed.

=== "Sync"

    ```Python hl_lines="6"
    # Import class from package
    from geoserverx._sync.gsx import SyncGeoServerX
    # Create class Instance with default paramaters
    client = SyncGeoServerX()
    # Get all workspaces in GeoServer
    client.get_all_workspaces()
    ```

=== "Async"

    ```Python hl_lines="6"
    # Import class from package
    from geoserverx._async.gsx import AsyncGeoServerX
    # Create class Instance with default paramaters
    client = AsyncGeoServerX()
    # Get all workspaces in GeoServer
    await client.get_all_workspaces()
    ```

=== "CLI"

    <div class="termy">

    ```console
    $ gsx workspaces --help

    Usage: gsx workspaces [OPTIONS]

    Get all workspaces in the Geoserver

    Options:
    --request [sync|async]  [default: requestEnum._sync]
    --url TEXT              Geoserver REST URL  [default:
                            http://127.0.0.1:8080/geoserver/rest/]
    --password TEXT         Geoserver Password  [default: GeoServer]
    --username TEXT         Geoserver username  [default: admin]
    --help                  Show this message and exit.
    ```

    </div>

## Get single workspace

This command fetches workspace with parameter as name of it from GeoServer.

=== "Sync"

    ```Python hl_lines="6"
    # Import class from package
    from geoserverx._sync.gsx import SyncGeoServerX
    # Create class Instance with default paramaters
    client = SyncGeoServerX()
    # Get workspace with name `cite`
    client.get_workspace('cite')
    ```

=== "Async"

    ```Python hl_lines="6"
    # Import class from package
    from geoserverx._async.gsx import AsyncGeoServerX
    # Create class Instance with default paramaters
    client = AsyncGeoServerX()
    # Get workspace with name `cite`
    await client.get_workspace('cite')
    ```

=== "CLI"

    <div class="termy">

    ```console
    $ gsx workspace cesium
    {"workspace": {"name": "cesium", "isolated": false, "dateCreated": "2023-02-13
    06:43:28.793 UTC", "dataStores":
    "http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/datastores.json",
    "coverageStores":
    "http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/coveragestores.json",
    "wmsStores": "http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/wmsstores.json",
    "wmtsStores": "http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/wmtsstores.json"}}
    ```

    </div>

## Create workspace

This command allows user to create new workspace.

| Parameter | Required                      | Default value | Data type | Description                                           |
| --------- | ----------------------------- | ------------- | --------- | ----------------------------------------------------- |
| Name      | :white_check_mark:            |               | `str`     | To define Name of the workspace                       |
| default   | :negative_squared_cross_mark: | `False`       | `bool`    | To define whether to keep workspace as default or not |
| isolated  | :negative_squared_cross_mark: | `False`       | `bool`    | To define whether to keep workspace as default or not |

=== "Sync"

    ```Python hl_lines="6"
    # Import class from package
    from geoserverx._sync.gsx import SyncGeoServerX
    # Create class Instance with default paramaters
    client = SyncGeoServerX()
    #Create new workspace with name `my_wrkspc` , make it Default and Isolated
    client.create_workspace(name='my_wrkspc',default=True,Isolated=True)
    ```

=== "Async"

    ```Python hl_lines="6"
    # Import class from package
    from geoserverx._async.gsx import AsyncGeoServerX
    # Create class Instance with default paramaters
    client = AsyncGeoServerX()
    #Create new workspace with name `my_wrkspc` , make it Default and Isolated
    await client.create_workspace(name='my_wrkspc',default=True,Isolated=True)
    ```

=== "CLI"

    <div class="termy">
    ```console
    $ gsx create-workspace my_wrkspc --default
    code=201 response='Data added successfully'
    ```
    </div>

## Delete workspace

This command allows user to delete workspace.

| Parameter | Required                      | Default value | Data type | Description                                                                                                                                           |
| --------- | ----------------------------- | ------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| workspace | :white_check_mark:            |               | `str`     | Name of the workspace                                                                                                                                 |
| recurse   | :negative_squared_cross_mark: | `False`       | `bool`    | This parameter recursively deletes all layers referenced by the specified workspace, including data stores, coverage stores, feature types, and so on |

=== "Sync"

    ```Python hl_lines="6"
    # Import class from package
    from geoserverx._sync.gsx import SyncGeoServerX
    # Create class Instance with default paramaters
    client = SyncGeoServerX()
    #Delete workspace with name `my_wrkspc`.
    client.delete_workspace(workspace='my_wrkspc',recurse=True)
    ```

=== "Async"

    ```Python hl_lines="6"
    # Import class from package
    from geoserverx._async.gsx import AsyncGeoServerX
    # Create class Instance with default paramaters
    client = AsyncGeoServerX()
    #Delete workspace with name `my_wrkspc`.
    await client.delete_workspace(workspace='my_wrkspc',recurse=True)
    ```

=== "CLI"

    <div class="termy">
    ```console
    gsx delete-workspace my_wrkspace --recurse
    {"code":200,"response":"Executed successfully"}
    ```
    </div>

## Update workspace

This command allows user to update existing workspace.

| Parameter | Required           | Data type                                                                                                                                             | Description                          |
| --------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| name      | :white_check_mark: | `str`                                                                                                                                                 | Name of the workspace to be updated  |
| update    | :white_check_mark: | [`UpdateWorkspaceInfo`](https://github.com/geobeyond/geoserverx/blob/b7757c9f0130864b06c40c2faa17afc841fc705f/src/geoserverx/models/workspace.py#L42) | To define body of the update request |

=== "Sync"

    ```Python hl_lines="3 7"
    # Import class from package
    from geoserverx._sync.gsx import SyncGeoServerX
    from geoserverx.models.workspace import UpdateWorkspaceInfo
    # Create class Instance with default paramaters
    client = SyncGeoServerX()
    # Updating workspace with name `my_wrkspc` , make is Isolated and rename it to `my_new_wrkspc`
    client.update_workspace(name='my_wrkspc',update=UpdateWorkspaceInfo(name='my_new_wrkspc',isolated=True))
    ```

=== "Async"

    ```Python hl_lines="3 7"
    # Import class from package
    from geoserverx._async.gsx import AsyncGeoServerX
    from geoserverx.models.workspace import UpdateWorkspaceInfo
    # Create class Instance with default paramaters
    client = AsyncGeoServerX()
    #Updating workspace with name `my_wrkspc` , make is Isolated and rename it to `my_new_wrkspc`
    await client.update_workspace(name='my_wrkspc',update=UpdateWorkspaceInfo(name='my_new_wrkspc',isolated=True))
    ```

=== "CLI"

    <div class="termy">
    ```console
    gsx update-workspace d --new-name duster
    {"code":200,"response":"Executed successfully"}
    ```
    </div>
