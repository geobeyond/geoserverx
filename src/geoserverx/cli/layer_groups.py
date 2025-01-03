import typer
from rich import print

from geoserverx._sync.gsx import SyncGeoServerX

layer_groups_app = typer.Typer()


@SyncGeoServerX.exception_handler
@layer_groups_app.command(help="Get All layer groups in the Geoserver")
def get(
    workspace: str,
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
