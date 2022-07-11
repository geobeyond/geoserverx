import httpx
from pydantic import ValidationError
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
    print("this should fail!")
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
    respx_mock.get(f"{baseUrl}workspaces").mock(side_effect=httpx.NetworkError)
    with pytest.raises(httpx.NetworkError):
        client.get_all_workspaces()


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


def test_get_workspace_NetworkError(client: SyncGeoServerX, respx_mock):
    respx_mock.get(f"{baseUrl}workspaces/pydad").mock(side_effect=httpx.ConnectError)
    response = client.get_workspace("pydad")
    assert response.response == "Error in connecting to Geoserver"


# @pytest_mark.anyio
# def test_get_vector_stores_in_workspaces_no_ws_fail(
#     client: SyncGeoServerX,
#     httpx_mock: HTTPXMock,
#     bad_datastore_item_connection
# ):
#     httpx_mock.add_response(json=bad_datastore_item_connection)
#     with pytest.raises(ValidationError):
#         store = client.get_vector_stores_in_workspaces('cisfte')

# @pytest_mark.anyio
# def test_get_vector_stores_in_workspaces_success(
#     client: SyncGeoServerX,
#     httpx_mock: HTTPXMock,
#     good_datastores_model_connection
# ):
#     httpx_mock.add_response(json=good_datastores_model_connection)
#     store = client.get_vector_stores_in_workspaces('jn')
#     assert isinstance(store.dataStores.dataStore, list)

# @pytest_mark.anyio
# def test_get_raster_stores_in_workspaces_no_store_fail(
#     client: SyncGeoServerX,
#     httpx_mock: HTTPXMock,
#     bad_coverages_stores_model_connection
# ):
#     httpx_mock.add_response(json=bad_coverages_stores_model_connection)
#     with pytest.raises(ValidationError):
#         store = client.get_raster_stores_in_workspaces('jay')

# @pytest_mark.anyio
# def test_get_raster_stores_in_workspaces_success(
#     client:SyncGeoServerX,
#     httpx_mock: HTTPXMock,
#     good_coverages_stores_model_connection
# ):
#     httpx_mock.add_response(json=good_coverages_stores_model_connection)
#     store = client.get_raster_stores_in_workspaces('cite')
#     assert isinstance(store.coverageStores.coverageStore, list)

# @pytest_mark.anyio
# def test_allstyles_success(
#     client:SyncGeoServerX,
#     httpx_mock: HTTPXMock,
#     good_all_styles_model_connection
# ):
#     httpx_mock.add_response(json=good_all_styles_model_connection)
#     allstyles = client.get_allstyles()
#     assert isinstance(allstyles.styles.style, list)

# @pytest_mark.anyio
# def test_allstyles_fail(
#     client:SyncGeoServerX,
#     httpx_mock: HTTPXMock,
#     bad_all_styles_model_connection
# ):
#     httpx_mock.add_response(json=bad_all_styles_model_connection)
#     with pytest.raises(ValidationError):
#         style = client.get_allstyles()

# @pytest_mark.anyio
# def test_style_success(
#     client:SyncGeoServerX,
#     httpx_mock: HTTPXMock,
#     good_style_model_connection
# ):
#     httpx_mock.add_response(json=good_style_model_connection)
#     style = client.get_style('burg')
#     assert style.style.name == 'burg'

# @pytest_mark.anyio
# def test_style_fail(
#     client:SyncGeoServerX,
#     httpx_mock: HTTPXMock,
#     bad_style_model_connection
# ):
#     httpx_mock.add_response(json=bad_style_model_connection)
#     with pytest.raises(ValidationError):
#         style = client.get_style('dssdgsg')
