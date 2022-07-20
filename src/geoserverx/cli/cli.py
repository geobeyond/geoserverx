
import typer
from enum import Enum
from geoserverx._sync.gsx import SyncGeoServerX
from rich.json import JSON
from rich.console import Console
console = Console()
from rich import print
import json

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


# get all workspaces
@SyncGeoServerX.exception_handler
@app.command(help="Get all workspaces in the Geoserver")
def workspaces(request:requestEnum = 'sync' ,
url:str=typer.Option("http://127.0.0.1:8080/geoserver/rest/",help="Geoserver REST URL"), 
password:str = typer.Option("geoserver", help="Geoserver Password"),
username:str=typer.Option("admin", help="Geoserver username")):
    """
    Get all workspaces in the Geoserver
    """
    if request.value == 'sync':
        client = SyncGeoServerX(username,password,url)
        result = json.loads(client.get_all_workspaces().json())
        if 'code' in result:
            typer.secho(result, fg=typer.colors.RED)
        else : 
            print(result)
    else : 
        typer.echo("Async support will be shortly")


# get workspace
@SyncGeoServerX.exception_handler
@app.command(help="Get workspace in the Geoserver")
def workspace(request:requestEnum = 'sync' ,
workspace:str = typer.Option(...,  help="Geoserver workspace"),
url:str=typer.Option("http://127.0.0.1:8080/geoserver/rest/",help="Geoserver REST URL"), 
password:str = typer.Option("geoserver", help="Geoserver Password"),
username:str=typer.Option("admin", help="Geoserver username")):
    """
    Get workspace in the Geoserver
    """
    if request.value == 'sync':
        client = SyncGeoServerX(username,password,url)
        result = json.loads(client.get_workspace(workspace).json())
        if 'code' in result:
            typer.secho(result, fg=typer.colors.RED)
        else : 
            print(result)
    else : 
        typer.echo("Async support will be shortly")


# create workspace
@SyncGeoServerX.exception_handler
@app.command(help="Add workspace in the Geoserver")
def create_workspace(request:requestEnum = 'sync' ,
workspace:str = typer.Option(...,  help="Geoserver workspace"),
default:bool = typer.Option(False,  help="Geoserver workspace"),
isolated:bool = typer.Option(False,  help="Geoserver workspace"),
url:str=typer.Option("http://127.0.0.1:8080/geoserver/rest/",help="Geoserver REST URL"), 
password:str = typer.Option("geoserver", help="Geoserver Password"),
username:str=typer.Option("admin", help="Geoserver username")):
    """
    Add workspace in the Geoserver
    looks like - gsx create-workspace --workspace <workspacename> --default/--no-default  --isolated/--no-isolated --username <username> --password <password>
    """
    if request.value == 'sync':
        client = SyncGeoServerX(username,password,url)
        result = json.loads(client.create_workspace(workspace,default,isolated).json())
        if result['code'] == 201 :
            typer.secho(result, fg=typer.colors.GREEN)
        else :
            typer.secho(result, fg=typer.colors.RED)
        
    else : 
        typer.echo("Async support will be shortly")


# Get vector stores in specific workspaces
@SyncGeoServerX.exception_handler
@app.command(help="Get vector stores in specific workspaces")
def vector_st_wp(request:requestEnum = 'sync' ,
workspace:str = typer.Option(...,  help="Geoserver workspace"),
url:str=typer.Option("http://127.0.0.1:8080/geoserver/rest/",help="Geoserver REST URL"), 
password:str = typer.Option("geoserver", help="Geoserver Password"),
username:str=typer.Option("admin", help="Geoserver username")):
    """
    Get vector stores in specific workspaces
    """
    if request.value == 'sync':
        client = SyncGeoServerX(username,password,url)
        result = json.loads(client.get_vector_stores_in_workspaces(workspace).json())
        if 'code' in result:
            typer.secho(result, fg=typer.colors.RED)
        else : 
            print(result)
    else : 
        typer.echo("Async support will be shortly")


# Get raster stores in specific workspaces
@SyncGeoServerX.exception_handler
@app.command(help="Get raster stores in specific workspaces")
def raster_st_wp(request:requestEnum = 'sync' ,
workspace:str = typer.Option(...,  help="Geoserver workspace"),
url:str=typer.Option("http://127.0.0.1:8080/geoserver/rest/",help="Geoserver REST URL"), 
password:str = typer.Option("geoserver", help="Geoserver Password"),
username:str=typer.Option("admin", help="Geoserver username")):
    """
    Get raster stores in specific workspaces
    """
    if request.value == 'sync':
        client = SyncGeoServerX(username,password,url)
        result = json.loads(client.get_raster_stores_in_workspaces(workspace).json())
        if 'code' in result:
            typer.secho(result, fg=typer.colors.RED)
        else : 
            print(result)
    else : 
        typer.echo("Async support will be shortly")


# Get vector store information in specific workspaces
@SyncGeoServerX.exception_handler
@app.command(help="Get vector store information in specific workspaces")
def vector_store(request:requestEnum = 'sync' ,
workspace:str = typer.Option(...,  help="Geoserver workspace"),
store:str = typer.Option(...,  help="Geoserver workspace"),
url:str=typer.Option("http://127.0.0.1:8080/geoserver/rest/",help="Geoserver REST URL"), 
password:str = typer.Option("geoserver", help="Geoserver Password"),
username:str=typer.Option("admin", help="Geoserver username")):
    """
    Get vector store information in specific workspaces
    """
    if request.value == 'sync':
        client = SyncGeoServerX(username,password,url)
        result = json.loads(client.get_vector_store(workspace,store).json())
        if 'code' in result:
            typer.secho(result, fg=typer.colors.RED)
        else : 
            print(result)
    else : 
        typer.echo("Async support will be shortly")
