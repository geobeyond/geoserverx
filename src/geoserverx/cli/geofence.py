import typer
from rich import print

from geoserverx._sync.gsx import SyncGeoServerX

geofence_app = typer.Typer()


@SyncGeoServerX.exception_handler
@geofence_app.command(help="Get all geofence rules in the Geoserver")
def list_rules(
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
@geofence_app.command(help="Get geofence rule in the Geoserver")
def get_rule(
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
