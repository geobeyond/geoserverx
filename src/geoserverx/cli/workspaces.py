from enum import Enum
from typing import Optional

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from geoserverx.models.workspace import UpdateWorkspaceInfo

from .._sync.gsx import SyncGeoServerX

console = Console()


class OutputFormats(str, Enum):
    json = "json"
    table = "table"


app = typer.Typer()


@app.command(help="Get all workspaces in the Geoserver")
def list(
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


@app.command(help="Get workspace in the Geoserver")
def get(
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


@app.command(help="Delete workspace in the Geoserver")
def delete(
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


@app.command(help="Add workspace in the Geoserver")
def create(
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


@app.command(help="Update workspace in the Geoserver")
def update(
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
