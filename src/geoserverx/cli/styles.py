import typer
from rich import print

from .._sync.gsx import SyncGeoServerX

app = typer.Typer()


@app.command(help="Get all styles in Geoserver")
def list(
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


@app.command(help="Get style in Geoserver")
def get(
    style: str,
    url: str = typer.Option(
        "http://127.0.0.1:8080/geoserver/rest/", help="Geoserver REST URL"
    ),
    password: str = typer.Option("geoserver", help="Geoserver Password"),
    username: str = typer.Option("admin", help="Geoserver username"),
):
    """
    Get style in Geoserver
    """
    client = SyncGeoServerX(username, password, url)
    result = client.get_style(style).model_dump_json()
    print(result)
