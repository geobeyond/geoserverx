from typer.testing import CliRunner
from geoserverx.cli.cli import app
import httpx

runner = CliRunner()

baseUrl = "http://127.0.0.1:8080/geoserver/rest/"


# Test - get_all_workspaces
def test_get_all_workspaces_validation(bad_workspaces_connection, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces").mock(
        return_value=httpx.Response(404, json=bad_workspaces_connection)
    )
    result = runner.invoke(app, ["workspaces"])
    assert "404" in result.stdout


def test_get_all_workspaces_success(good_workspaces_connection, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces").mock(
        return_value=httpx.Response(200, json=good_workspaces_connection)
    )
    result = runner.invoke(app, ["workspaces"])
    assert "pydad" in result.stdout


def test_get_all_workspaces_NetworkError(respx_mock):
    respx_mock.get(f"{baseUrl}workspaces").mock(side_effect=httpx.ConnectError)
    result = runner.invoke(app, ["workspaces"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - get_workspace
def test_get_workspace_validation(bad_workspace_connection, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/sfsf").mock(
        return_value=httpx.Response(404, json=bad_workspace_connection)
    )
    result = runner.invoke(app, ["workspace", "--workspace", "sfsf"])
    assert "Result not found" in result.stdout


def test_get_workspace_success(good_workspace_connection, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/pydad").mock(
        return_value=httpx.Response(200, json=good_workspace_connection)
    )
    result = runner.invoke(app, ["workspace", "--workspace", "pydad"])
    assert "pydad" in result.stdout


def test_get_workspace_ConnectError(respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/pydad").mock(side_effect=httpx.ConnectError)
    result = runner.invoke(app, ["workspace", "--workspace", "pydad"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - get_vector_stores_in_workspaces
def test_get_vector_stores_in_workspaces_validation(
    invalid_datastores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores").mock(
        return_value=httpx.Response(404, json=invalid_datastores_model_connection)
    )
    result = runner.invoke(app, ["vector-st-wp", "--workspace", "sfsf"])
    assert "Result not found" in result.stdout


def test_get_vector_stores_in_workspaces_success(
    good_datastores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores").mock(
        return_value=httpx.Response(200, json=good_datastores_model_connection)
    )
    result = runner.invoke(app, ["vector-st-wp", "--workspace", "sfsf"])
    assert "jumper" in result.stdout


def test_get_vector_stores_in_workspaces_ConnectError(respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores").mock(
        side_effect=httpx.ConnectError
    )
    result = runner.invoke(app, ["vector-st-wp", "--workspace", "sfsf"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - get_raster_stores_in_workspaces
def test_get_raster_stores_in_workspaces_validation(
    invalid_coverages_stores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/coveragestores").mock(
        return_value=httpx.Response(404, json=invalid_coverages_stores_model_connection)
    )
    result = runner.invoke(app, ["raster-st-wp", "--workspace", "sfsf"])
    assert "Result not found" in result.stdout


def test_get_raster_stores_in_workspaces_success(
    good_coverages_stores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/coveragestores").mock(
        return_value=httpx.Response(200, json=good_coverages_stores_model_connection)
    )
    result = runner.invoke(app, ["raster-st-wp", "--workspace", "sfsf"])
    assert "RGB_125" in result.stdout


def test_get_raster_stores_in_workspaces_ConnectError(respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/coveragestores").mock(
        side_effect=httpx.ConnectError
    )
    result = runner.invoke(app, ["raster-st-wp", "--workspace", "sfsf"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - get_vector_store
def test_get_vector_store_validation(invalid_datastore_model_connection, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores/jumper.json").mock(
        return_value=httpx.Response(404, json=invalid_datastore_model_connection)
    )
    result = runner.invoke(
        app, ["vector-store", "--workspace", "sfsf", "--store", "jumper"]
    )
    assert "Result not found" in result.stdout


def test_get_vector_store_success(good_datastore_model_connection, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores/jumper.json").mock(
        return_value=httpx.Response(200, json=good_datastore_model_connection)
    )
    result = runner.invoke(
        app, ["vector-store", "--workspace", "sfsf", "--store", "jumper"]
    )
    assert "jumper" in result.stdout


def test_get_vector_store_ConnectError(respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores/jumper.json").mock(
        side_effect=httpx.ConnectError
    )
    result = runner.invoke(
        app, ["vector-store", "--workspace", "sfsf", "--store", "jumper"]
    )
    assert "Error in connecting to Geoserver" in result.stdout


# Test - get_raster_store
def test_get_raster_store_validation(
    invalid_coverages_store_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/cite/coveragestores/RGB_125.json").mock(
        return_value=httpx.Response(404, json=invalid_coverages_store_model_connection)
    )
    result = runner.invoke(
        app, ["raster-store", "--workspace", "cite", "--store", "RGB_125"]
    )
    assert "Result not found" in result.stdout


def test_get_raster_store_success(good_coverages_store_model_connection, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/cite/coveragestores/RGB_125.json").mock(
        return_value=httpx.Response(200, json=good_coverages_store_model_connection)
    )
    result = runner.invoke(
        app, ["raster-store", "--workspace", "cite", "--store", "RGB_125"]
    )
    assert "RGB_125" in result.stdout


def test_get_raster_store_ConnectError(respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/cite/coveragestores/RGB_125.json").mock(
        side_effect=httpx.ConnectError
    )
    result = runner.invoke(
        app, ["raster-store", "--workspace", "cite", "--store", "RGB_125"]
    )
    assert "Error in connecting to Geoserver" in result.stdout


# Test - get_allstyles
def test_get_allstyles_validation(invalid_all_styles_model_connection, respx_mock):
    respx_mock.get(f"{baseUrl}styles").mock(
        return_value=httpx.Response(404, json=invalid_all_styles_model_connection)
    )
    result = runner.invoke(app, ["styles"])
    assert "Result not found" in result.stdout


def test_get_allstyles_success(good_all_styles_model_connection, respx_mock):
    respx_mock.get(f"{baseUrl}styles").mock(
        return_value=httpx.Response(200, json=good_all_styles_model_connection)
    )
    result = runner.invoke(app, ["styles"])
    assert "CUSD 2020 Census Blocks" in result.stdout


def test_get_allstyles_ConnectError(respx_mock):
    respx_mock.get(f"{baseUrl}styles").mock(side_effect=httpx.ConnectError)
    result = runner.invoke(app, ["styles"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - get_style
def test_get_style_validation(invalid_style_model_connection, respx_mock):
    respx_mock.get(f"{baseUrl}styles/burg.json").mock(
        return_value=httpx.Response(404, json=invalid_style_model_connection)
    )
    result = runner.invoke(app, ["style", "--style", "burg"])
    assert "Result not found" in result.stdout


def test_get_style_success(good_style_model_connection, respx_mock):
    respx_mock.get(f"{baseUrl}styles/burg.json").mock(
        return_value=httpx.Response(200, json=good_style_model_connection)
    )
    result = runner.invoke(app, ["style", "--style", "burg"])
    assert "burg" in result.stdout


def test_get_style_ConnectError(respx_mock):
    respx_mock.get(f"{baseUrl}styles/burg.json").mock(side_effect=httpx.ConnectError)
    result = runner.invoke(app, ["style", "--style", "burg"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - create_workspace
def test_create_workspace_validation(invalid_new_workspace_connection, respx_mock):
    respx_mock.post(f"{baseUrl}workspaces?default=False").mock(
        return_value=httpx.Response(404, json=invalid_new_workspace_connection)
    )
    result = runner.invoke(
        app,
        ["create-workspace", "--workspace", "burg", "--no-default", "--no-isolated"],
    )
    assert "Result not found" in result.stdout


def test_create_workspace_success(good_new_workspace_connection, respx_mock):
    respx_mock.post(f"{baseUrl}workspaces?default=False").mock(
        return_value=httpx.Response(201, json=good_new_workspace_connection)
    )
    result = runner.invoke(
        app, ["create-workspace", "--workspace", "pydad", "--no-default", "--isolated"]
    )
    assert "Data added successfully" in result.stdout


def test_create_workspace_ConnectError(respx_mock):
    respx_mock.post(f"{baseUrl}workspaces?default=False").mock(
        side_effect=httpx.ConnectError
    )
    result = runner.invoke(
        app, ["create-workspace", "--workspace", "pydad", "--no-default", "--isolated"]
    )
    assert "Error in connecting to Geoserver" in result.stdout

# Test - pg_store
def test_pg_store_validation(invalid_new_pg_store_connection, respx_mock):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        return_value=httpx.Response(404, json=invalid_new_pg_store_connection)
    )
    result = runner.invoke(
        app,
        ["create-pg-store", "--name", "pgg", "--workspace", "cesium", "--dbname", "postgres","--dbpwd", "postgres"],
    )
    assert "Result not found" in result.stdout


def test_pg_store_success(good_new_workspace_connection, respx_mock):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        return_value=httpx.Response(201, json=good_new_workspace_connection)
    )
    result = runner.invoke(
        app, ["create-pg-store", "--name", "pgg", "--workspace", "cesium", "--dbname", "postgres","--dbpwd", "postgres"]
    )
    assert "Data added successfully" in result.stdout


def test_pg_store_ConnectError(respx_mock):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        side_effect=httpx.ConnectError
    )
    result = runner.invoke(
        app, ["create-pg-store", "--name", "pgg", "--workspace", "cesium", "--dbname", "postgres","--dbpwd", "postgres" ]
    )
    assert "Error in connecting to Geoserver" in result.stdout
