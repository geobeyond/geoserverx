import httpx, respx
from pytest import mark as pytest_mark
from geoserverx.models.workspace import WorkspaceInBulk
from geoserverx._async.gsx import AsyncGeoServerX, GeoServerXAuth, GeoServerXError
import pytest_asyncio
import pytest
from respx.fixtures import session_event_loop as event_loop  # noqa: F401

baseUrl = "http://127.0.0.1:8080/geoserver/rest/"

from respx.fixtures import session_event_loop as event_loop  # noqa: F401


@pytest_asyncio.fixture(scope="session")
async def create_a_client():
    client = AsyncGeoServerX.from_auth(GeoServerXAuth())
    yield client
    client.close()


#
@pytest_mark.anyio
async def test_error():
    try:
        client = AsyncGeoServerX(url="", username="", password="")
        assert False
    except GeoServerXError:
        assert True


@pytest.mark.asyncio
async def test_get_all_workspaces_validation(
    create_a_client, respx_mock, bad_workspaces_connection, event_loop
):
    respx_mock.get(f"{baseUrl}workspaces").mock(
        return_value=httpx.Response(404, json=bad_workspaces_connection)
    )
    response = await create_a_client.get_all_workspaces()
    assert response.code == 404


@pytest.mark.asyncio
async def test_get_all_workspaces_success(
    create_a_client, respx_mock, good_workspaces_connection, event_loop
):
    respx_mock.get(f"{baseUrl}workspaces").mock(
        return_value=httpx.Response(200, json=good_workspaces_connection)
    )
    response = await create_a_client.get_all_workspaces()
    assert response.workspaces.workspace[0].name == "pydad"


@pytest.mark.asyncio
async def test_get_all_workspaces_NetworkError(create_a_client, respx_mock):
    respx.get(f"{baseUrl}workspaces").mock(side_effect=httpx.ConnectError)
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.get_all_workspaces()
        assert response.response == "Error in connecting to Geoserver"


# Test - get_workspace
@pytest_mark.anyio
async def test_get_workspace_validation(
    create_a_client, bad_workspace_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf").mock(
        return_value=httpx.Response(404, json=bad_workspace_connection)
    )
    response = await create_a_client.get_workspace("sfsf")
    assert response.response == "Result not found"


@pytest_mark.anyio
async def test_get_workspace_success(
    create_a_client, good_workspace_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/pydad").mock(
        return_value=httpx.Response(200, json=good_workspace_connection)
    )
    response = await create_a_client.get_workspace("pydad")
    assert response.workspace.name == "pydad"


@pytest_mark.anyio
async def test_get_workspace_ConnectError(create_a_client, respx_mock):
    respx.get(f"{baseUrl}workspaces/pydad").mock(side_effect=httpx.ConnectError)
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.get_workspace("pydad")
        assert response.response == "Error in connecting to Geoserver"


# Test - get_vector_stores_in_workspaces
@pytest_mark.anyio
async def test_get_vector_stores_in_workspaces_validation(
    create_a_client, invalid_datastores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores").mock(
        return_value=httpx.Response(404, json=invalid_datastores_model_connection)
    )
    response = await create_a_client.get_vector_stores_in_workspaces("sfsf")
    assert response.response == "Result not found"


@pytest_mark.anyio
async def test_get_vector_stores_in_workspaces_success(
    create_a_client, good_datastores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores").mock(
        return_value=httpx.Response(200, json=good_datastores_model_connection)
    )
    response = await create_a_client.get_vector_stores_in_workspaces("sfsf")
    assert response.dataStores.dataStore[0].name == "jumper"


@pytest_mark.anyio
async def test_get_vector_stores_in_workspaces_ConnectError(
    create_a_client, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores").mock(
        side_effect=httpx.ConnectError
    )
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.get_vector_stores_in_workspaces("sfsf")
        assert response.response == "Error in connecting to Geoserver"


# Test - get_raster_stores_in_workspaces
@pytest_mark.anyio
async def test_get_raster_stores_in_workspaces_validation(
    create_a_client, invalid_coverages_stores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/coveragestores").mock(
        return_value=httpx.Response(404, json=invalid_coverages_stores_model_connection)
    )
    response = await create_a_client.get_raster_stores_in_workspaces("sfsf")
    assert response.response == "Result not found"


@pytest_mark.anyio
async def test_get_raster_stores_in_workspaces_success(
    create_a_client, good_coverages_stores_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/coveragestores").mock(
        return_value=httpx.Response(200, json=good_coverages_stores_model_connection)
    )
    response = await create_a_client.get_raster_stores_in_workspaces("sfsf")
    assert response.coverageStores.coverageStore[0].name == "RGB_125"


@pytest_mark.anyio
async def test_get_raster_stores_in_workspaces_ConnectError(
    create_a_client, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/coveragestores").mock(
        side_effect=httpx.ConnectError
    )
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.get_raster_stores_in_workspaces("sfsf")
        assert response.response == "Error in connecting to Geoserver"


# Test - get_vector_store
@pytest_mark.anyio
async def test_get_vector_store_validation(
    create_a_client, invalid_datastore_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores/jumper.json").mock(
        return_value=httpx.Response(404, json=invalid_datastore_model_connection)
    )
    response = await create_a_client.get_vector_store("sfsf", "jumper")
    assert response.response == "Result not found"


@pytest_mark.anyio
async def test_get_vector_store_success(
    create_a_client, good_datastore_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores/jumper.json").mock(
        return_value=httpx.Response(200, json=good_datastore_model_connection)
    )
    response = await create_a_client.get_vector_store("sfsf", "jumper")
    assert response.dataStore.name == "jumper"


@pytest_mark.anyio
async def test_get_vector_store_ConnectError(create_a_client, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/sfsf/datastores/jumper.json").mock(
        side_effect=httpx.ConnectError
    )
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.get_vector_store("sfsf", "jumper")
        assert response.response == "Error in connecting to Geoserver"


# Test - get_raster_store
@pytest_mark.anyio
async def test_get_raster_store_validation(
    create_a_client, invalid_coverages_store_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/cite/coveragestores/RGB_125.json").mock(
        return_value=httpx.Response(404, json=invalid_coverages_store_model_connection)
    )
    response = await create_a_client.get_raster_store("cite", "RGB_125")
    assert response.response == "Result not found"


@pytest_mark.anyio
async def test_get_raster_store_success(
    create_a_client, good_coverages_store_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}workspaces/cite/coveragestores/RGB_125.json").mock(
        return_value=httpx.Response(200, json=good_coverages_store_model_connection)
    )
    response = await create_a_client.get_raster_store("cite", "RGB_125")
    assert response.coverageStore.name == "RGB_125"


@pytest_mark.anyio
async def test_get_raster_store_ConnectError(create_a_client, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/cite/coveragestores/RGB_125.json").mock(
        side_effect=httpx.ConnectError
    )
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.get_raster_store("cite", "RGB_125")
        assert response.response == "Error in connecting to Geoserver"


# Test - get_allstyles
@pytest_mark.anyio
async def test_get_allstyles_validation(
    create_a_client, invalid_all_styles_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}styles").mock(
        return_value=httpx.Response(404, json=invalid_all_styles_model_connection)
    )
    response = await create_a_client.get_allstyles()
    assert response.response == "Result not found"


@pytest_mark.anyio
async def test_get_allstyles_success(
    create_a_client, good_all_styles_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}styles").mock(
        return_value=httpx.Response(200, json=good_all_styles_model_connection)
    )
    response = await create_a_client.get_allstyles()
    assert response.styles.style[0].name == "CUSD 2020 Census Blocks"


@pytest_mark.anyio
async def test_get_allstyles_ConnectError(create_a_client, respx_mock):
    respx_mock.get(f"{baseUrl}styles").mock(side_effect=httpx.ConnectError)
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.get_allstyles()
        assert response.response == "Error in connecting to Geoserver"


# Test - get_style
@pytest_mark.anyio
async def test_get_style_validation(
    create_a_client, invalid_style_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}styles/burg.json").mock(
        return_value=httpx.Response(404, json=invalid_style_model_connection)
    )
    response = await create_a_client.get_style("burg")
    assert response.response == "Result not found"


@pytest_mark.anyio
async def test_get_style_success(
    create_a_client, good_style_model_connection, respx_mock
):
    respx_mock.get(f"{baseUrl}styles/burg.json").mock(
        return_value=httpx.Response(200, json=good_style_model_connection)
    )
    response = await create_a_client.get_style("burg")
    assert response.style.name == "burg"


@pytest_mark.anyio
async def test_get_style_ConnectError(create_a_client, respx_mock):
    respx_mock.get(f"{baseUrl}styles/burg.json").mock(side_effect=httpx.ConnectError)
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.get_style("burg")
        assert response.response == "Error in connecting to Geoserver"


# Test - create_workspace
@pytest_mark.anyio
async def test_create_workspace_validation(
    create_a_client, invalid_new_workspace_connection, respx_mock
):
    respx_mock.post(f"{baseUrl}workspaces?default=False").mock(
        return_value=httpx.Response(404, json=invalid_new_workspace_connection)
    )
    response = await create_a_client.create_workspace("pydad", False, True)
    assert response.response == "Result not found"


@pytest_mark.anyio
async def test_create_workspace_success(
    create_a_client, good_new_workspace_connection, respx_mock
):
    respx_mock.post(f"{baseUrl}workspaces?default=False").mock(
        return_value=httpx.Response(201, json=good_new_workspace_connection)
    )
    response = await create_a_client.create_workspace("pydad", False, True)
    assert response.response == "Data added successfully"


@pytest_mark.anyio
async def test_create_workspace_ConnectError(create_a_client, respx_mock):
    respx_mock.post(f"{baseUrl}workspaces?default=False").mock(
        side_effect=httpx.ConnectError
    )
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.create_workspace("pydad", False, True)
        assert response.response == "Error in connecting to Geoserver"


# # Test - create_pg_store
@pytest_mark.anyio
async def test_create_pg_store_validation(
    create_a_client, invalid_new_pg_store_connection, respx_mock
):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        return_value=httpx.Response(404, json=invalid_new_pg_store_connection)
    )
    response = await create_a_client.create_pg_store(
        name="pgg",
        workspace="cesium",
        host="localhost",
        port=5432,
        username="postgres",
        password="postgres",
        database="postgres",
    )
    assert response.response == "Result not found"


@pytest_mark.anyio
async def test_create_pg_store_success(
    create_a_client, good_new_workspace_connection, respx_mock
):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        return_value=httpx.Response(201, json=good_new_workspace_connection)
    )
    response = await create_a_client.create_pg_store(
        name="pgg",
        workspace="cesium",
        host="localhost",
        port=5432,
        username="postgres",
        password="postgres",
        database="postgres",
    )
    assert response.response == "Data added successfully"


@pytest_mark.anyio
async def test_create_pg_store_ConnectError(create_a_client, respx_mock):
    respx_mock.post(f"{baseUrl}workspaces/cesium/datastores/").mock(
        side_effect=httpx.ConnectError
    )
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.create_pg_store(
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
@pytest.mark.asyncio
async def test_get_all_layers_validation(
    create_a_client, respx_mock, bad_layers_connection, event_loop
):
    respx_mock.get(f"{baseUrl}layers").mock(
        return_value=httpx.Response(404, json=bad_layers_connection)
    )
    response = await create_a_client.get_all_layers()
    assert response.code == 404


@pytest.mark.asyncio
async def test_get_all_layers_success(
    create_a_client, respx_mock, good_layers_connection, event_loop
):
    respx_mock.get(f"{baseUrl}layers").mock(
        return_value=httpx.Response(200, json=good_layers_connection)
    )
    response = await create_a_client.get_all_layers()
    assert response.layers.layer[0].name == "tiger:giant_polygon"


@pytest.mark.asyncio
async def test_get_all_layers_NetworkError(create_a_client, respx_mock):
    respx.get(f"{baseUrl}layers").mock(side_effect=httpx.ConnectError)
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.get_all_layers()
        assert response.response == "Error in connecting to Geoserver"


# Test - get_layer
@pytest.mark.asyncio
async def test_get_layer_validation(
    create_a_client, respx_mock, bad_layer_connection, event_loop
):
    respx_mock.get(f"{baseUrl}layers/tiger:poi").mock(
        return_value=httpx.Response(404, json=bad_layer_connection)
    )
    response = await create_a_client.get_layer(workspace="tiger", layer="poi")
    assert response.code == 404


@pytest.mark.asyncio
async def test_get_layer_success(
    create_a_client, respx_mock, good_layer_connection, event_loop
):
    respx_mock.get(f"{baseUrl}layers/tiger:poi").mock(
        return_value=httpx.Response(200, json=good_layer_connection)
    )
    response = await create_a_client.get_layer(workspace="tiger", layer="poi")
    assert response.layer.name == "poi"


@pytest.mark.asyncio
async def test_get_layer_NetworkError(create_a_client, respx_mock):
    respx.get(f"{baseUrl}layers/tiger:poi").mock(side_effect=httpx.ConnectError)
    with pytest.raises(httpx.ConnectError):
        response = await create_a_client.get_layer(workspace="tiger", layer="poi")
        assert response.response == "Error in connecting to Geoserver"
