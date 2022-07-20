from typer.testing import CliRunner
from geoserverx.cli.cli import app

runner = CliRunner()

# get workspaces
def test_workspaces():
    result = runner.invoke(app, ["workspaces"])
    assert result.exit_code == 0