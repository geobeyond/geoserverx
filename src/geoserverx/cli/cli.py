import typer
from enum import Enum
from geoserverx._sync.gsx import SyncGeoServerX
from rich import print
import json
from pathlib import Path

app = typer.Typer()


@app.callback()
def callback():
    """
    GeoserverX CLI tools to talk to Geoserver efficiently .
    """


# Enum for request type
class requestEnum(str, Enum):
    _sync = "sync"
    _async = "async"


# Enum for vector file type
class vectorFileEnum(str, Enum):
    shapefile = "shapefile"
    gpkg = "gpkg"


# get all workspaces
@SyncGeoServerX.exception_handler
@app.command(help="Get all workspaces in the Geoserver")
def workspaces(
    request: requestEnum = requestEnum._sync,
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get all workspaces in the Geoserver
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.get_all_workspaces().json()
        if "code" in result:
            typer.secho(result, fg=typer.colors.RED)
        else:
            print(result)
    else:
        typer.echo("Async support will be shortly")


# get workspace
@SyncGeoServerX.exception_handler
@app.command(help="Get workspace in the Geoserver")
def workspace(
    request: requestEnum = requestEnum._sync,
    workspace: str = typer.Option(..., help="Workspace name"),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get workspace in the Geoserver
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.get_workspace(workspace).json()
        if "code" in result:
            typer.secho(result, fg=typer.colors.RED)
        else:
            print(result)
    else:
        typer.echo("Async support will be shortly")


# create workspace
@SyncGeoServerX.exception_handler
@app.command(help="Add workspace in the Geoserver")
def create_workspace(
    request: requestEnum = requestEnum._sync,
    workspace: str = typer.Option(..., help="Workspace name"),
    default: bool = typer.Option(False, help="Make workspace default?"),
    isolated: bool = typer.Option(False, help="Make workspace isolated?"),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Add workspace in the Geoserver
    looks like - gsx create-workspace --workspace <workspacename> --default/--no-default  --isolated/--no-isolated --username <username> --password <password>
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.create_workspace(workspace, default, isolated).json()
        if json.loads(result)["code"] == 201:
            typer.secho(result, fg=typer.colors.GREEN)
        else:
            typer.secho(result, fg=typer.colors.RED)

    else:
        typer.echo("Async support will be shortly")


# Get vector stores in specific workspaces
@SyncGeoServerX.exception_handler
@app.command(help="Get vector stores in specific workspaces")
def vector_st_wp(
    request: requestEnum = requestEnum._sync,
    workspace: str = typer.Option(..., help="Workspace name"),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get vector stores in specific workspaces
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.get_vector_stores_in_workspaces(workspace).json()
        if "code" in result:
            typer.secho(result, fg=typer.colors.RED)
        else:
            print(result)
    else:
        typer.echo("Async support will be shortly")


# Get raster stores in specific workspaces
@SyncGeoServerX.exception_handler
@app.command(help="Get raster stores in specific workspaces")
def raster_st_wp(
    request: requestEnum = requestEnum._sync,
    workspace: str = typer.Option(..., help="Workspace name"),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get raster stores in specific workspaces
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.get_raster_stores_in_workspaces(workspace).json()
        if "code" in result:
            typer.secho(result, fg=typer.colors.RED)
        else:
            print(result)
    else:
        typer.echo("Async support will be shortly")


# Get vector store information in specific workspaces
@SyncGeoServerX.exception_handler
@app.command(help="Get vector store information in specific workspaces")
def vector_store(
    request: requestEnum = requestEnum._sync,
    workspace: str = typer.Option(..., help="Workspace name"),
    store: str = typer.Option(..., help="Store name"),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get vector store information in specific workspaces
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.get_vector_store(workspace, store).json()
        if "code" in result:
            typer.secho(result, fg=typer.colors.RED)
        else:
            print(result)
    else:
        typer.echo("Async support will be shortly")


# Get raster store information in specific workspaces
@SyncGeoServerX.exception_handler
@app.command(help="Get raster store information in specific workspaces")
def raster_store(
    request: requestEnum = requestEnum._sync,
    workspace: str = typer.Option(..., help="Workspace name"),
    store: str = typer.Option(..., help="Store name"),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get raster store information in specific workspaces
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.get_raster_store(workspace, store).json()
        if "code" in result:
            typer.secho(result, fg=typer.colors.RED)
        else:
            print(result)
    else:
        typer.echo("Async support will be shortly")


# Get all styles in Geoserver
@SyncGeoServerX.exception_handler
@app.command(help="Get all styles in Geoserver")
def styles(
    request: requestEnum = requestEnum._sync,
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get all styles in Geoserver
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.get_allstyles().json()
        if "code" in result:
            typer.secho(result, fg=typer.colors.RED)
        else:
            print(result)
    else:
        typer.echo("Async support will be shortly")


# Get style in Geoserver
@SyncGeoServerX.exception_handler
@app.command(help="Get style in Geoserver")
def style(
    request: requestEnum = requestEnum._sync,
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    style: str = typer.Option(..., help="Style name"),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get style in Geoserver
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.get_style(style).json()
        if "code" in result:
            typer.secho(result, fg=typer.colors.RED)
        else:
            print(result)
    else:
        typer.echo("Async support will be shortly")


# Create Vector Layer in Geoserver
@SyncGeoServerX.exception_handler
@app.command(help="Create Vector Layer in Geoserver")
def create_file(
    request: requestEnum = requestEnum._sync,
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    workspace: str = typer.Option(..., help="Workspace name"),
    store: str = typer.Option(..., help="Store name"),
    service_type: vectorFileEnum = typer.Option(..., help="Vector file type"),
    file: Path = typer.Option(..., help="File path"),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Create Vector Layer in Geoserver
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        try:
            files = open(file, "rb")
            result = client.create_file_store(
                workspace, store, files.read(), service_type
            )
            if result.code == 201:
                typer.secho(result, fg=typer.colors.GREEN)
            else:
                typer.secho(result, fg=typer.colors.RED)
        except:
            typer.secho("File path is incorrect", fg=typer.colors.YELLOW)
    else:
        typer.echo("Async support will be shortly")


# Create PostgreSQL store in Geoserver
@SyncGeoServerX.exception_handler
@app.command(help="Create PostgreSQL store in Geoserver")
def create_pg_store(
    request: requestEnum = requestEnum._sync,
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    name: str = typer.Option(..., help="Store name"),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
    workspace: str = typer.Option(..., help="workspace name"),
    host: str = typer.Option("localhost", help="Host IP Address"),
    port: int = typer.Option(5432, help="Database port"),
    dbuser: str = typer.Option("postgres", help="Database username"),
    dbname: str = typer.Option(..., help="Database name"),
    dbpwd: str = typer.Option(..., help="Database password"),
):
    """
    Create PostgreSQL store in Geoserver
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.create_pg_store(
            name=name,
            workspace=workspace,
            host=host,
            port=port,
            username=dbuser,
            password=dbpwd,
            database=dbname,
        )
        if result.code == 201:
            typer.secho(result, fg=typer.colors.GREEN)
        else:
            typer.secho(result, fg=typer.colors.RED)
    else:
        typer.echo("Async support will be shortly")


# get all layers
@SyncGeoServerX.exception_handler
@app.command(help="Get all layers in the Geoserver")
def layers(
    request: requestEnum = requestEnum._sync,
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    workspace: str = typer.Option(None, help="Workspace name"),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get all layers in the Geoserver
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.get_all_layers(workspace).json()
        if "code" in result:
            typer.secho(result, fg=typer.colors.RED)
        else:
            print(result)
    else:
        typer.echo("Async support will be shortly")


# get layer
@SyncGeoServerX.exception_handler
@app.command(help="Get layer in the Geoserver")
def layer(
    request: requestEnum = requestEnum._sync,
    workspace: str = typer.Option(..., help="Workspace name"),
    layer: str = typer.Option(..., help="Layer name"),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get workspace in the Geoserver
    """
    if request.value == "sync":
        client = SyncGeoServerX(username, password, url)
        result = client.get_layer(workspace, layer).json()
        if "code" in result:
            typer.secho(result, fg=typer.colors.RED)
        else:
            print(result)
    else:
        typer.echo("Async support will be shortly")
