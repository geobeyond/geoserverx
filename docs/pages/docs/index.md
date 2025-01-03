---
hide:
  - toc
---

# Using geoserverx

`geoserverx` allows user to call methods synchronously, asynchronously as well as via CLI.

## Setup Class instance

=== "Sync"

    ```Python
    # Import class from package
    from geoserverx._sync.gsx import SyncGeoServerX
    # Create class Instance with default paramaters
    client = SyncGeoServerX()
    ```

=== "Async"

    ```Python
    # Import class from package
    from geoserverx._async.gsx import AsyncGeoServerX
    # Create class Instance with default paramaters
    client = AsyncGeoServerX()
    ```

=== "CLI"

    <div class="termy">

    ```console

    pip install geoserverx

    ---> 100%

    $ gsx --help
    Usage: gsx [OPTIONS] COMMAND [ARGS]...

    GeoserverX CLI tools to talk to Geoserver efficiently .

    Options:
    --install-completion [bash|zsh|fish|powershell|pwsh]
                                    Install completion for the specified shell.
    --show-completion [bash|zsh|fish|powershell|pwsh]
                                    Show completion for the specified shell, to
                                    copy it or customize the installation.
    --help                          Show this message and exit.

    Commands:
    create-file       Create Vector Layer in Geoserver
    create-workspace  Add workspace in the Geoserver
    raster-st-wp      Get raster stores in specific workspaces
    raster-store      Get raster store information in specific workspaces
    style             Get style in Geoserver
    styles            Get all styles in Geoserver
    vector-st-wp      Get vector stores in specific workspaces
    vector-store      Get vector store information in specific workspaces
    workspace         Get workspace in the Geoserver
    workspaces        Get all workspaces in the Geoserver
    ```

    </div>

These paramaters however can be changed as follows

=== "Sync"

    ```Python
    # Import class from package
    from geoserverx._sync.gsx import SyncGeoServerX
    # Create class Instance with custom paramaters
    client = SyncGeoServerX(username='mygeos', password='SecuredPass',url='http://127.0.0.1:9090/geoserver/rest/')
    ```

=== "Async"

    ```Python
    # Import class from package
    from geoserverx._async.gsx import AsyncGeoServerX
    # Create class Instance with custom paramaters
    client = AsyncGeoServerX(username='mygeos', password='SecuredPass',url='http://127.0.0.1:9090/geoserver/rest/')
    ```

This class can also be used as context manager to manage the opening and closing connection automatically.

=== "Sync"

    ```Python
    # Import class from package
    from geoserverx._sync.gsx import SyncGeoServerX
    # Create class Instance with custom paramaters
    client = SyncGeoServerX(username='mygeos', password='SecuredPass',url='http://127.0.0.1:9090/geoserver/rest/')

    #Using with as
    with client as cl :
        response = cl.get_all_workspaces()
    ```

=== "Async"

    ```Python
    # Import class from package
    from geoserverx._async.gsx import  AsyncGeoServerX,GeoServerXAuth
    import asyncio
    # Create class Instance with custom paramaters
    client = AsyncGeoServerX(username='mygeos', password='SecuredPass',url='http://127.0.0.1:9090/geoserver/rest/')

    #Using with as
    async def main():
            async with client as cl:
                    response = await cl.get_all_workspaces()
                    print(response)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    ```
