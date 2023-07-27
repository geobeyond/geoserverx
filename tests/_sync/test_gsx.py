import httpx
from pytest import fixture, mark as pytest_mark
import pytest
from geoserverx.models.workspace import WorkspaceInBulk
from geoserverx._sync.gsx import SyncGeoServerX, GeoServerXAuth, GeoServerXError


baseUrl = "http://127.0.0.1:8080/geoserver/rest/"


@fixture(name="client")
def create_client():
    client = SyncGeoServerX.from_auth(GeoServerXAuth())
    yield client
    client.close()


@pytest_mark.anyio
def test_error():
    try:
        client = SyncGeoServerX(url="", username="", password="")
        assert False
    except GeoServerXError:
        assert True


# Test - get_all_workspaces
def test_get_all_workspaces_validation(
    client: SyncGeoServerX, bad_workspaces_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces").mock(
        return_value=httpx.Response(404, json=bad_workspaces_connection)
    )
    response = client.get_all_workspaces()
    assert response.code == 404


def test_get_all_workspaces_success(
    client: SyncGeoServerX, good_workspaces_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces").mock(
        return_value=httpx.Response(200, json=good_workspaces_connection)
    )
    response = client.get_all_workspaces()
    assert response.workspaces.workspace[0].name == "pydad"


def test_get_all_workspaces_NetworkError(client: SyncGeoServerX, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces").mock(side_effect=httpx.ConnectError)
    response = client.get_all_workspaces()
    assert response.response == "Error in connecting to Geoserver"


# Test - get_workspace
def test_get_workspace_validation(
    client: SyncGeoServerX, bad_workspace_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf").mock(
        return_value=httpx.Response(404, json=bad_workspace_connection)
    )
    response = client.get_workspace("sfsf")
    assert response.response == "Result not found"


def test_get_workspace_success(
    client: SyncGeoServerX, good_workspace_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/pydad").mock(
        return_value=httpx.Response(200, json=good_workspace_connection)
    )
    response = client.get_workspace("pydad")
    assert response.workspace.name == "pydad"


def test_get_workspace_ConnectError(client: SyncGeoServerX, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/pydad").mock(side_effect=httpx.ConnectError)
    response = client.get_workspace("pydad")
    assert response.response == "Error in connecting to Geoserver"


# Test - get_vector_stores_in_workspaces
def test_get_vector_stores_in_workspaces_validation(
    client: SyncGeoServerX, invalid_datastores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores").mock(
        return_value=httpx.Response(404, json=invalid_datastores_model_connection)
    )
    response = client.get_vector_stores_in_workspaces("sfsf")
    assert response.response == "Result not found"


def test_get_vector_stores_in_workspaces_success(
    client: SyncGeoServerX, good_datastores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores").mock(
        return_value=httpx.Response(200, json=good_datastores_model_connection)
    )
    response = client.get_vector_stores_in_workspaces("sfsf")
    assert response.dataStores.dataStore[0].name == "jumper"


def test_get_vector_stores_in_workspaces_ConnectError(
    client: SyncGeoServerX, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores").mock(
        side_effect=httpx.ConnectError
    )
    response = client.get_vector_stores_in_workspaces("sfsf")
    assert response.response == "Error in connecting to Geoserver"


# Test - get_raster_stores_in_workspaces
def test_get_raster_stores_in_workspaces_validation(
    client: SyncGeoServerX, invalid_coverages_stores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/coveragestores").mock(
        return_value=httpx.Response(404, json=invalid_coverages_stores_model_connection)
    )
    response = client.get_raster_stores_in_workspaces("sfsf")
    assert response.response == "Result not found"


def test_get_raster_stores_in_workspaces_success(
    client: SyncGeoServerX, good_coverages_stores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/coveragestores").mock(
        return_value=httpx.Response(200, json=good_coverages_stores_model_connection)
    )
    response = client.get_raster_stores_in_workspaces("sfsf")
    assert response.coverageStores.coverageStore[0].name == "RGB_125"


def test_get_raster_stores_in_workspaces_ConnectError(
    client: SyncGeoServerX, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/coveragestores").mock(
        side_effect=httpx.ConnectError
    )
    response = client.get_raster_stores_in_workspaces("sfsf")
    assert response.response == "Error in connecting to Geoserver"


# Test - get_vector_store
def test_get_vector_store_validation(
    client: SyncGeoServerX, invalid_datastore_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores/jumper.json").mock(
        return_value=httpx.Response(404, json=invalid_datastore_model_connection)
    )
    response = client.get_vector_store("sfsf", "jumper")
    assert response.response == "Result not found"


def test_get_vector_store_success(
    client: SyncGeoServerX, good_datastore_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores/jumper.json").mock(
        return_value=httpx.Response(200, json=good_datastore_model_connection)
    )
    response = client.get_vector_store("sfsf", "jumper")
    assert response.dataStore.name == "jumper"


def test_get_vector_store_ConnectError(client: SyncGeoServerX, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores/jumper.json").mock(
        side_effect=httpx.ConnectError
    )
    response = client.get_vector_store("sfsf", "jumper")
    assert response.response == "Error in connecting to Geoserver"


# Test - get_raster_store
def test_get_raster_store_validation(
    client: SyncGeoServerX, invalid_coverages_store_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/cite/coveragestores/RGB_125.json").mock(
        return_value=httpx.Response(404, json=invalid_coverages_store_model_connection)
    )
    response = client.get_raster_store("cite", "RGB_125")
    assert response.response == "Result not found"


def test_get_raster_store_success(
    client: SyncGeoServerX, good_coverages_store_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/cite/coveragestores/RGB_125.json").mock(
        return_value=httpx.Response(200, json=good_coverages_store_model_connection)
    )
    response = client.get_raster_store("cite", "RGB_125")
    assert response.coverageStore.name == "RGB_125"


def test_get_raster_store_ConnectError(client: SyncGeoServerX, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/cite/coveragestores/RGB_125.json").mock(
        side_effect=httpx.ConnectError
    )
    response = client.get_raster_store("cite", "RGB_125")
    assert response.response == "Error in connecting to Geoserver"


# Test - get_allstyles
def test_get_allstyles_validation(
    client: SyncGeoServerX, invalid_all_styles_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}styles").mock(
        return_value=httpx.Response(404, json=invalid_all_styles_model_connection)
    )
    response = client.get_allstyles()
    assert response.response == "Result not found"


def test_get_allstyles_success(
    client: SyncGeoServerX, good_all_styles_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}styles").mock(
        return_value=httpx.Response(200, json=good_all_styles_model_connection)
    )
    response = client.get_allstyles()
    assert response.styles.style[0].name == "CUSD 2020 Census Blocks"


def test_get_allstyles_ConnectError(client: SyncGeoServerX, respx_mock):
    respx_mock.get(f"{baseUrl}styles").mock(side_effect=httpx.ConnectError)
    response = client.get_allstyles()
    assert response.response == "Error in connecting to Geoserver"


# Test - get_style
def test_get_style_validation(
    client: SyncGeoServerX, invalid_style_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}styles/burg.json").mock(
        return_value=httpx.Response(404, json=invalid_style_model_connection)
    )
    response = client.get_style("burg")
    assert response.response == "Result not found"


def test_get_style_success(
    client: SyncGeoServerX, good_style_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}styles/burg.json").mock(
        return_value=httpx.Response(200, json=good_style_model_connection)
    )
    response = client.get_style("burg")
    assert response.style.name == "burg"


def test_get_style_ConnectError(client: SyncGeoServerX, respx_mock):
    respx_mock.get(f"{baseUrl}styles/burg.json").mock(side_effect=httpx.ConnectError)
    response = client.get_style("burg")
    assert response.response == "Error in connecting to Geoserver"


# Test - create_workspace
def test_create_workspace_validation(
    client: SyncGeoServerX, invalid_new_workspace_connection, respx_mock
):
    respx_mock.post(f"{baseUrl}workspaces?default=False").mock(
        return_value=httpx.Response(404, json=invalid_new_workspace_connection)
    )
    response = client.create_workspace("pydad", False, True)
    assert response.response == "Result not found"


def test_create_workspace_success(
    client: SyncGeoServerX, good_new_workspace_connection, respx_mock
):
    respx_mock.post(f"{baseUrl}workspaces?default=False").mock(
        return_value=httpx.Response(201, json=good_new_workspace_connection)
    )
    response = client.create_workspace("pydad", False, True)
    assert response.response == "Data added successfully"


def test_create_workspace_ConnectError(client: SyncGeoServerX, respx_mock):
    respx_mock.post(f"{baseUrl}workspaces?default=False").mock(
        side_effect=httpx.ConnectError
    )
    response = client.create_workspace("pydad", False, True)
    assert response.response == "Error in connecting to Geoserver"


# Test - create_pg_store
def test_create_pg_store_validation(
    client: SyncGeoServerX, invalid_new_pg_store_connection, respx_mock
):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        return_value=httpx.Response(404, json=invalid_new_pg_store_connection)
    )
    response = client.create_pg_store(
        name="pgg",
        workspace="cesium",
        host="localhost",
        port=5432,
        username="postgres",
        password="postgres",
        database="postgres",
    )
    assert response.response == "Result not found"


def test_create_pg_store_success(
    client: SyncGeoServerX, good_new_workspace_connection, respx_mock
):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        return_value=httpx.Response(201, json=good_new_workspace_connection)
    )
    response = client.create_pg_store(
        name="pgg",
        workspace="cesium",
        host="localhost",
        port=5432,
        username="postgres",
        password="postgres",
        database="postgres",
    )
    assert response.response == "Data added successfully"


def test_create_pg_store_ConnectError(client: SyncGeoServerX, respx_mock):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        side_effect=httpx.ConnectError
    )
    response = client.create_pg_store(
        name="pgg",
        workspace="cesium",
        host="localhost",
        port=5432,
        username="postgres",
        password="postgres",
        database="postgres",
    )
    assert response.response == "Error in connecting to Geoserver"



# Test - get_all_layers
def test_get_all_layers_validation(
    client: SyncGeoServerX, bad_layers_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}layers").mock(
        return_value=httpx.Response(404, json=bad_layers_connection)
    )
    response = client.get_all_layers()
    assert response.code == 404


def test_get_all_layers_success(
    client: SyncGeoServerX, good_layers_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}layers").mock(
        return_value=httpx.Response(200, json=good_layers_connection)
    )
    response = client.get_all_layers()
    assert response.layers.layer[0].name == "tiger:giant_polygon"


def test_get_all_layers_NetworkError(client: SyncGeoServerX, respx_mock):
    respx_mock.get(f"{baseUrl}layers").mock(side_effect=httpx.ConnectError)
    response = client.get_all_layers()
    assert response.response == "Error in connecting to Geoserver"


# Test - get_layer
def test_get_layer_validation(
    client: SyncGeoServerX, bad_layer_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}layers/tiger:poi").mock(
        return_value=httpx.Response(404, json=bad_layer_connection)
    )
    response = client.get_layer(workspace="tiger", layer="poi")
    assert response.response == "Result not found"


def test_get_layer_success(
    client: SyncGeoServerX, good_layer_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}layers/tiger:poi").mock(
        return_value=httpx.Response(200, json=good_layer_connection)
    )
    response = client.get_layer(workspace="tiger", layer="poi")
    assert response.layer.name == "poi"


def test_get_layer_ConnectError(client: SyncGeoServerX, respx_mock):
    respx_mock.get(f"{baseUrl}layers/tiger:poi").mock(side_effect=httpx.ConnectError)
    response = client.get_layer(workspace="tiger", layer="poi")
    assert response.response == "Error in connecting to Geoserver"