import httpx
import pytest
from typer.testing import CliRunner

from geoserverx.cli.cli import app

runner = CliRunner()

baseUrl = "http://127.0.0.1:8080/geoserver/rest/"


# Test - workspaces
def test_get_all_workspaces_success(respx_mock):
    """Test getting all workspaces"""
    # Test data
    workspace_response = {
        "workspaces": {
            "workspace": [
                {
                    "name": "aa",
                    "href": "http://127.0.0.1:8080/geoserver/rest/workspaces/aa.json",
                },
                {
                    "name": "aaba",
                    "href": "http://127.0.0.1:8080/geoserver/rest/workspaces/aaba.json",
                },
            ]
        }
    }
    # Mock the response
    respx_mock.get(f"{baseUrl}workspaces").mock(
        return_value=httpx.Response(200, json=workspace_response)
    )
    # Invoke the command
    result = runner.invoke(app, ["workspaces", "--output", "json"])
    # Assertions
    assert result.exit_code == 0
    for workspace in workspace_response["workspaces"]["workspace"]:
        assert workspace["name"] in result.output


# Test - get_workspace
@pytest.mark.parametrize(
    "workspace_name,status_code,response_data,expected_response",
    [
        (
            "sfsf",
            404,
            {"code": 404, "response": "Result not found"},
            "Result not found",
        ),
    ],
)
def test_get_workspace_validation(
    workspace_name, status_code, response_data, expected_response, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/{workspace_name}").mock(
        return_value=httpx.Response(status_code, json=response_data)
    )
    result = runner.invoke(app, ["workspace", "sfsf"])
    assert expected_response in result.stdout


def test_get_workspace_success(good_workspace_connection, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/pydad").mock(
        return_value=httpx.Response(200, json=good_workspace_connection)
    )
    result = runner.invoke(app, ["workspace", "pydad"])
    assert "pydad" in result.stdout


def test_get_workspace_ConnectError(respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/pydad").mock(side_effect=httpx.ConnectError)
    result = runner.invoke(app, ["workspace", "pydad"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - update_workspace
@pytest.mark.parametrize(
    "workspace_name,status_code,response_data,expected_response",
    [
        (
            "tiger",
            404,
            {"code": 404, "response": "Result not found"},
            "Result not found",
        ),
    ],
)
def test_update_workspace_validation(
    respx_mock, workspace_name, status_code, response_data, expected_response
):
    respx_mock.put(f"{baseUrl}workspaces/{workspace_name}.json").mock(
        return_value=httpx.Response(status_code, json=response_data)
    )
    result = runner.invoke(app, ["update-workspace", workspace_name, "--isolated"])
    assert expected_response in result.stdout


@pytest.mark.parametrize(
    "workspace_name,workspace_info,status_code,response_data",
    [
        (
            "tiger",
            "--isolated",
            200,
            "Executed successfully",
        )
    ],
)
def test_update_workspace_success(
    respx_mock, workspace_name, workspace_info, status_code, response_data
):
    respx_mock.put(f"{baseUrl}workspaces/{workspace_name}.json").mock(
        return_value=httpx.Response(status_code, json=response_data)
    )
    print(workspace_info)
    result = runner.invoke(app, ["update-workspace", workspace_name, workspace_info])
    assert response_data in result.stdout


def test_update_workspace_ConnectError(respx_mock):
    respx_mock.put(f"{baseUrl}workspaces/tiger.json").mock(
        side_effect=httpx.ConnectError
    )
    result = runner.invoke(app, ["update-workspace", "tiger", "--isolated"])
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


# Test - get_all_styles
def test_get_all_styles_validation(invalid_all_styles_model_connection, respx_mock):
    respx_mock.get(f"{baseUrl}styles").mock(
        return_value=httpx.Response(404, json=invalid_all_styles_model_connection)
    )
    result = runner.invoke(app, ["styles"])
    assert "Result not found" in result.stdout


def test_get_all_styles_success(good_all_styles_model_connection, respx_mock):
    respx_mock.get(f"{baseUrl}styles").mock(
        return_value=httpx.Response(200, json=good_all_styles_model_connection)
    )
    result = runner.invoke(app, ["styles"])
    assert "CUSD 2020 Census" in result.stdout


def test_get_all_styles_ConnectError(respx_mock):
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
    respx_mock.post(f"{baseUrl}workspaces", params={"default": False}).mock(
        return_value=httpx.Response(404, json=invalid_new_workspace_connection)
    )
    result = runner.invoke(
        app,
        ["create-workspace", "burg", "--no-default", "--no-isolated"],
    )
    assert "Result not found" in result.stdout


def test_create_workspace_success(good_new_workspace_connection, respx_mock):
    respx_mock.post(f"{baseUrl}workspaces", params={"default": False}).mock(
        return_value=httpx.Response(201, json=good_new_workspace_connection)
    )
    result = runner.invoke(
        app, ["create-workspace", "pydad", "--no-default", "--isolated"]
    )
    assert "Data added successfully" in result.stdout


def test_create_workspace_ConnectError(respx_mock):
    respx_mock.post(f"{baseUrl}workspaces", params={"default": False}).mock(
        side_effect=httpx.ConnectError
    )
    result = runner.invoke(
        app, ["create-workspace", "pydad", "--no-default", "--isolated"]
    )
    assert "Error in connecting to Geoserver" in result.stdout


# Test - pg_store
def test_pg_store_validation(invalid_new_pg_store_connection, respx_mock):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        return_value=httpx.Response(404, json=invalid_new_pg_store_connection)
    )
    result = runner.invoke(
        app,
        [
            "create-pg-store",
            "--name",
            "pgg",
            "--workspace",
            "cesium",
            "--dbname",
            "postgres",
            "--dbpwd",
            "postgres",
        ],
    )
    assert "Result not found" in result.stdout


def test_pg_store_success(good_new_workspace_connection, respx_mock):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        return_value=httpx.Response(201, json=good_new_workspace_connection)
    )
    result = runner.invoke(
        app,
        [
            "create-pg-store",
            "--name",
            "pgg",
            "--workspace",
            "cesium",
            "--dbname",
            "postgres",
            "--dbpwd",
            "postgres",
        ],
    )
    assert "Data added successfully" in result.stdout


def test_pg_store_ConnectError(respx_mock):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        side_effect=httpx.ConnectError
    )
    result = runner.invoke(
        app,
        [
            "create-pg-store",
            "--name",
            "pgg",
            "--workspace",
            "cesium",
            "--dbname",
            "postgres",
            "--dbpwd",
            "postgres",
        ],
    )
    assert "Error in connecting to Geoserver" in result.stdout


# Test - get_all_layers
def test_get_all_layers_validation(bad_layers_connection, respx_mock):
    respx_mock.get(f"{baseUrl}layers").mock(
        return_value=httpx.Response(404, json=bad_layers_connection)
    )
    result = runner.invoke(app, ["layers"])
    assert "404" in result.stdout


def test_get_all_layers_success(good_layers_connection, respx_mock):
    respx_mock.get(f"{baseUrl}layers").mock(
        return_value=httpx.Response(200, json=good_layers_connection)
    )
    result = runner.invoke(app, ["layers"])
    assert "tiger:giant_polygon" in result.stdout


def test_get_all_layers_NetworkError(respx_mock):
    respx_mock.get(f"{baseUrl}layers").mock(side_effect=httpx.ConnectError)
    result = runner.invoke(app, ["layers"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - get_layer
def test_get_layer_validation(bad_layer_connection, respx_mock):
    respx_mock.get(f"{baseUrl}layers/tiger:poi").mock(
        return_value=httpx.Response(404, json=bad_layer_connection)
    )
    result = runner.invoke(app, ["layer", "--workspace", "tiger", "--layer", "poi"])
    assert "404" in result.stdout


def test_get_layer_success(good_layer_connection, respx_mock):
    respx_mock.get(f"{baseUrl}layers/tiger:poi").mock(
        return_value=httpx.Response(200, json=good_layer_connection)
    )
    result = runner.invoke(app, ["layer", "--workspace", "tiger", "--layer", "poi"])
    assert "poi" in result.stdout


def test_get_layer_NetworkError(respx_mock):
    respx_mock.get(f"{baseUrl}layers/tiger:poi").mock(side_effect=httpx.ConnectError)
    result = runner.invoke(app, ["layer", "--workspace", "tiger", "--layer", "poi"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - get_all_layer_groups
def test_get_all_layer_groups_validation(bad_layer_groups_connection, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/ne/layergroups").mock(
        return_value=httpx.Response(404, json=bad_layer_groups_connection)
    )
    result = runner.invoke(app, ["layer-groups", "--workspace", "ne"])
    assert "404" in result.stdout


def test_get_all_layer_groups_success(good_layer_groups_connection, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/ne/layergroups").mock(
        return_value=httpx.Response(200, json=good_layer_groups_connection)
    )
    result = runner.invoke(app, ["layer-groups", "--workspace", "ne"])
    assert "tg" in result.stdout


def test_get_all_layer_groups_NetworkError(respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/ne/layergroups").mock(
        side_effect=httpx.ConnectError
    )
    result = runner.invoke(app, ["layer-groups", "--workspace", "ne"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - reset_geoserver
def test_reset_geoserver_validation(bad_reset_geoserver_connection, respx_mock):
    respx_mock.put(f"{baseUrl}reset").mock(
        return_value=httpx.Response(404, json=bad_reset_geoserver_connection)
    )
    result = runner.invoke(app, ["reset"])
    assert "404" in result.stdout


def test_reset_geoserver_success(good_reset_geoserver_connection, respx_mock):
    respx_mock.put(f"{baseUrl}reset").mock(
        return_value=httpx.Response(200, json=good_reset_geoserver_connection)
    )
    result = runner.invoke(app, ["reset"])
    assert "200" in result.stdout


def test_reset_geoserver_NetworkError(respx_mock):
    respx_mock.put(f"{baseUrl}reset").mock(side_effect=httpx.ConnectError)
    result = runner.invoke(app, ["reset"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - reload_geoserver
def test_reload_geoserver_validation(bad_reload_geoserver_connection, respx_mock):
    respx_mock.put(f"{baseUrl}reload").mock(
        return_value=httpx.Response(404, json=bad_reload_geoserver_connection)
    )
    result = runner.invoke(app, ["reload"])
    assert "404" in result.stdout


def test_reload_geoserver_success(good_reload_geoserver_connection, respx_mock):
    respx_mock.put(f"{baseUrl}reload").mock(
        return_value=httpx.Response(200, json=good_reload_geoserver_connection)
    )
    result = runner.invoke(app, ["reload"])
    assert "200" in result.stdout


def test_reload_geoserver_NetworkError(respx_mock):
    respx_mock.put(f"{baseUrl}reload").mock(side_effect=httpx.ConnectError)
    result = runner.invoke(app, ["reload"])
    assert "Error in connecting to Geoserver" in result.stdout


# Test - all_geofence_rules
def test_all_geofence_rules_validation(bad_all_geofence_rules_connection, respx_mock):
    respx_mock.get(f"{baseUrl}about/status.json").mock(
        return_value=httpx.Response(
            200, json={"statuss": {"status": [{"name": "geofence"}]}}
        )
    )
    respx_mock.get(
        f"{baseUrl}geofence/rules/", headers={"Accept": "application/json"}
    ).mock(return_value=httpx.Response(404, json=bad_all_geofence_rules_connection))
    result = runner.invoke(app, ["geofence-rules"])
    assert "404" in result.stdout


def test_all_geofence_rules_success(good_all_geofence_rules_connection, respx_mock):
    respx_mock.get(f"{baseUrl}about/status.json").mock(
        return_value=httpx.Response(
            200, json={"statuss": {"status": [{"name": "geofence"}]}}
        )
    )
    respx_mock.get(
        f"{baseUrl}geofence/rules/", headers={"Accept": "application/json"}
    ).mock(return_value=httpx.Response(200, json=good_all_geofence_rules_connection))
    result = runner.invoke(app, ["geofence-rules"])
    assert "2" in result.stdout


def test_all_geofence_rules_NetworkError(respx_mock):
    respx_mock.get(f"{baseUrl}about/status.json").mock(
        return_value=httpx.Response(
            200, json={"statuss": {"status": [{"name": "geofence"}]}}
        )
    )
    respx_mock.get(
        f"{baseUrl}geofence/rules/", headers={"Accept": "application/json"}
    ).mock(side_effect=httpx.ConnectError)
    result = runner.invoke(app, ["geofence-rules"])
    assert "Error in connecting to Geoserver" in result.stdout
