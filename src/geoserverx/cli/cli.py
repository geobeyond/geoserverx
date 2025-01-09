import typer

from .geofence import app as geofence_app
from .layer_groups import app as layer_groups_app
from .layers import app as layers_app
from .stores import app as stores_app
from .styles import app as styles_app
from .workspaces import app as workspaces_app

app = typer.Typer()
app.add_typer(workspaces_app, name="workspaces")
app.add_typer(styles_app, name="styles")
app.add_typer(layers_app, name="layers")
app.add_typer(geofence_app, name="geofence")
app.add_typer(stores_app, name="stores")
app.add_typer(layer_groups_app, name="layer-groups")


@app.callback()
def callback():
    """
    GeoserverX CLI tools to talk to Geoserver efficiently .
    """
