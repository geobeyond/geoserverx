
import typer
from enum import Enum

from geoserverx._sync.gsx import SyncGeoServerX


app = typer.Typer()


@app.callback()
def callback():
    """
    GeoserverX CLI tools to talk to Geoserver efficiently .
    """


# Enum for request type
class requestEnum(str,Enum):
    sync_call = 'sync'
    async_call = 'async'

@app.command()
def workspaces(request:requestEnum ,url:str="http://127.0.0.1:8080/geoserver/rest/", password:str = 'geoserver', username:str='admin'):
    """
    Get all workspaces in the Geoserver
    """
    if request.value == 'sync':
        client = SyncGeoServerX(username,password,url)
        typer.echo(client.get_all_workspaces())
    else : 
        typer.echo("Async support will be shortly")

