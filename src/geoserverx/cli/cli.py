from enum import Enum
from pathlib import Path
from typing import Optional

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from .._sync.gsx import SyncGeoServerX
from ..models.workspace import UpdateWorkspaceInfo

app = typer.Typer()
console = Console()


class OutputFormats(str, Enum):
    json = "json"
    table = "table"


@app.callback()
def callback():
    """
    GeoserverX CLI tools to talk to Geoserver efficiently .
    """


# Enum for vector file type
class VectorFileEnum(str, Enum):
    shapefile = "shapefile"
    gpkg = "gpkg"


@SyncGeoServerX.exception_handler
@app.command(help="Get all workspaces in the Geoserver")
def workspaces(
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
    output: OutputFormats = typer.Option(OutputFormats.table),
):
    """
    Get all workspaces in the Geoserver
    looks like - gsx workspaces --url <url> --username <username> --password <password>
    """
    client = SyncGeoServerX(username, password, url)
    result = client.get_all_workspaces()
    if "code" in result:
        print(result)
    else:
        if output == "json":
            print(result.model_dump_json(indent=2))
        else:
            try:
                table = Table("Name", "Link")
                for workspace in result.workspaces.workspace:
                    table.add_row(workspace.name, workspace.href)
                console.print(table)
            except AttributeError:
                print(result.response)


@SyncGeoServerX.exception_handler
@app.command(help="Get workspace in the Geoserver")
def workspace(
    workspace: str,
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
    output: OutputFormats = typer.Option(OutputFormats.table),
):
    """
    Get workspace in the Geoserver
    looks like - gsx workspace  <workspacename> --url <url> --username <username> --password <password>
    """

    client = SyncGeoServerX(username, password, url)
    result = client.get_workspace(workspace)
    if "code" in result:
        print(result)
    else:
        if output == "json":
            print(result.model_dump_json(indent=2))
        else:
            try:
                table = Table("Column", "Value")
                table.add_row("name", result.workspace.name)
                table.add_row("isolated", str(result.workspace.isolated))
                table.add_row("dateCreated", result.workspace.dateCreated)
                table.add_row("dataStores", result.workspace.dataStores)
                table.add_row("coverageStores", result.workspace.coverageStores)
                table.add_row("wmsStores", result.workspace.wmsStores)
                table.add_row("wmtsStores", result.workspace.wmtsStores)
                console.print(table)
            except AttributeError:
                print(result.response)


@SyncGeoServerX.exception_handler
@app.command(help="Delete workspace in the Geoserver")
def delete_workspace(
    workspace: str,
    recurse: bool = typer.Option(False, help="Delete all stores,layers,styles,etc."),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Delete workspace in the Geoserver
    looks like - gsx delete-workspace  <workspacename> --recurse/--no-recurse --url <url> --username <username> --password <password>
    """
    client = SyncGeoServerX(username, password, url)
    result = client.delete_workspace(workspace, recurse)
    print(result.response)


@SyncGeoServerX.exception_handler
@app.command(help="Add workspace in the Geoserver")
def create_workspace(
    workspace: str,
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
    looks like - gsx create-workspace  <workspacename> --default/--no-default  --isolated/--no-isolated --url <url> --username <username> --password <password>
    """

    client = SyncGeoServerX(username, password, url)
    result = client.create_workspace(workspace, default, isolated)
    print(result.response)


@SyncGeoServerX.exception_handler
@app.command(help="Add workspace in the Geoserver")
def update_workspace(
    current_name: str,
    new_name: Optional[str] = typer.Option(None, help="New Workspace name"),
    isolated: Optional[bool] = typer.Option(False, help="Make workspace isolated?"),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Update existing workspace in the Geoserver
    looks like - gsx update-workspace  <workspacename> --new-name <new-workspacename> --isolated/--no-isolated --username <username> --password <password>
    """

    client = SyncGeoServerX(username, password, url)
    result = client.update_workspace(
        current_name,
        UpdateWorkspaceInfo(name=new_name, isolated=isolated),
    )
    print(result.response)


@SyncGeoServerX.exception_handler
@app.command(help="Get vector stores in specific workspaces")
def vector_st_wp(
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

    client = SyncGeoServerX(username, password, url)
    result = client.get_vector_stores_in_workspaces(workspace).model_dump_json()
    print(result)


@SyncGeoServerX.exception_handler
@app.command(help="Get raster stores in specific workspaces")
def raster_st_wp(
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

    client = SyncGeoServerX(username, password, url)
    result = client.get_raster_stores_in_workspaces(workspace).model_dump_json()
    print(result)


@SyncGeoServerX.exception_handler
@app.command(help="Get vector store information in specific workspaces")
def vector_store(
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
    client = SyncGeoServerX(username, password, url)
    result = client.get_vector_store(workspace, store).model_dump_json()
    print(result)


@SyncGeoServerX.exception_handler
@app.command(help="Get raster store information in specific workspaces")
def raster_store(
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
    client = SyncGeoServerX(username, password, url)
    result = client.get_raster_store(workspace, store).model_dump_json()
    print(result)


@SyncGeoServerX.exception_handler
@app.command(help="Get all styles in Geoserver")
def styles(
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get all styles in Geoserver
    """
    client = SyncGeoServerX(username, password, url)
    result = client.get_all_styles().model_dump_json()
    print(result)


@SyncGeoServerX.exception_handler
@app.command(help="Get style in Geoserver")
def style(
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
    client = SyncGeoServerX(username, password, url)
    result = client.get_style(style).model_dump_json()
    print(result)


@SyncGeoServerX.exception_handler
@app.command(help="Create Vector Layer in Geoserver")
def create_file(
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    workspace: str = typer.Option(..., help="Workspace name"),
    store: str = typer.Option(..., help="Store name"),
    service_type: VectorFileEnum = typer.Option(..., help="Vector file type"),
    file: Path = typer.Option(..., help="File path"),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Create Vector Layer in Geoserver
    """
    client = SyncGeoServerX(username, password, url)
    try:
        files = open(file, "rb")
        result = client.create_file_store(workspace, store, files.read(), service_type)
        print(result)
    except Exception:
        print("File path is incorrect")


@SyncGeoServerX.exception_handler
@app.command(help="Create PostgreSQL store in Geoserver")
def create_pg_store(
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
    print(result)


@SyncGeoServerX.exception_handler
@app.command(help="Get all layers in the Geoserver")
def layers(
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
    client = SyncGeoServerX(username, password, url)
    result = client.get_all_layers(workspace).model_dump_json()
    print(result)


@SyncGeoServerX.exception_handler
@app.command(help="Get layer in the Geoserver")
def layer(
    workspace: str = typer.Option(..., help="Workspace name"),
    layer: str = typer.Option(..., help="Layer name"),
    detail: bool = typer.Option(False, help="Detail Info"),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get workspace in the Geoserver
    """
    client = SyncGeoServerX(username, password, url)
    result = client.get_layer(workspace, layer, detail).model_dump_json()
    print(result)


@SyncGeoServerX.exception_handler
@app.command(help="Get layer groups in the Geoserver")
def layer_groups(
    workspace: str = typer.Option(default=None, help="Workspace name"),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get layer groups in the Geoserver
    """
    client = SyncGeoServerX(username, password, url)
    result = client.get_all_layer_groups(workspace).json()
    print(result)


@SyncGeoServerX.exception_handler
@app.command(help="Get all geofence rules in the Geoserver")
def geofence_rules(
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get all geofence rules in the Geoserver
    """
    client = SyncGeoServerX(username, password, url)
    result = client.get_all_geofence_rules().model_dump_json()
    print(result)


@SyncGeoServerX.exception_handler
@app.command(help="Get geofence rule in the Geoserver")
def geofence_rule(
    id: int = typer.Option(..., help="Geofence rule id"),
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get geofence rule in the Geoserver
    """
    client = SyncGeoServerX(username, password, url)
    result = client.get_geofence_rule(id).model_dump_json()
    print(result)
