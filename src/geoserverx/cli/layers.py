import typer
from rich import print

from .._sync.gsx import SyncGeoServerX

app = typer.Typer()


@app.command(help="Get all layers in the Geoserver")
def list(
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


@app.command(help="Get layer in the Geoserver")
def get(
    workspace: str,
    layer: str,
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
