from enum import Enum
from pathlib import Path

import typer
from rich import print

from geoserverx._sync.gsx import SyncGeoServerX


# Enum for vector file type
class vectorFileEnum(str, Enum):
    shapefile = "shapefile"
    gpkg = "gpkg"


stores_app = typer.Typer()


@SyncGeoServerX.exception_handler
@stores_app.command(help="Get vector stores in specific workspaces")
def workspace_vector_stores(
    workspace: str,
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
@stores_app.command(help="Get raster stores in specific workspaces")
def workspace_raster_stores(
    workspace: str,
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
@stores_app.command(help="Get vector store information in specific workspaces")
def get_vector_store(
    workspace: str,
    store: str,
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
@stores_app.command(help="Get raster store information in specific workspaces")
def get_raster_store(
    workspace: str,
    store: str,
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
@stores_app.command(help="Create Vector Layer in Geoserver")
def create_vector_store(
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
    client = SyncGeoServerX(username, password, url)
    try:
        files = open(file, "rb")
        result = client.create_file_store(workspace, store, files.read(), service_type)
        print(result)
    except Exception:
        print("File path is incorrect")


@SyncGeoServerX.exception_handler
@stores_app.command(help="Create PostgreSQL store in Geoserver")
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
