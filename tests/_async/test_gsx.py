from pydantic import ValidationError
from pytest import fixture, mark as pytest_mark
import pytest
from pytest_httpx import HTTPXMock
from geoserverx.models.workspace import WorkspaceInBulk
from geoserverx._async.gsx import (
    AsyncGeoServerX, GeoServerXAuth, GeoServerXError
)


@fixture(name="client")
async def create_client():
    client = AsyncGeoServerX.from_auth(GeoServerXAuth())
    yield client
    await client.close()

@pytest_mark.anyio
async def test_error():
    try:
        client = AsyncGeoServerX(
            url="", username="", password="")
        assert False
    except GeoServerXError:
        assert True


@pytest_mark.anyio
async def test_all_workspaces(
    client: AsyncGeoServerX,
    httpx_mock: HTTPXMock,
    good_workspaces_connection
):
    httpx_mock.add_response(json=good_workspaces_connection)
    allwork = await client.get_all_workspaces()
    if len(allwork.workspaces.workspace) > 0:
        assert isinstance(allwork.workspaces.workspace[0], WorkspaceInBulk)
    else :
        assert isinstance(allwork.workspaces.workspace, list) 


@pytest_mark.anyio
async def test_workspace_success(
    client: AsyncGeoServerX,
    httpx_mock: HTTPXMock,
    good_workspace_connection
):
    httpx_mock.add_response(json=good_workspace_connection)
    worksp = await client.get_workspace('pydad')
    assert worksp.workspace.name == 'pydad'

@pytest_mark.anyio
async def test_workspace_fail(
    client: AsyncGeoServerX,
    httpx_mock: HTTPXMock,
    bad_workspace_connection
):
    httpx_mock.add_response(json=bad_workspace_connection)
    with pytest.raises(ValidationError):
        worksp = await client.get_workspace('sfsf')

@pytest_mark.anyio
async def test_get_vector_stores_in_workspaces_no_ws_fail(
    client: AsyncGeoServerX,
    httpx_mock: HTTPXMock,
    bad_datastore_item_connection
):
    httpx_mock.add_response(json=bad_datastore_item_connection)
    with pytest.raises(ValidationError):
        store = await client.get_vector_stores_in_workspaces('cisfte')

@pytest_mark.anyio
async def test_get_vector_stores_in_workspaces_success(
    client: AsyncGeoServerX,
    httpx_mock: HTTPXMock,
    good_datastores_model_connection
):
    httpx_mock.add_response(json=good_datastores_model_connection)
    store = await client.get_vector_stores_in_workspaces('jn')
    assert isinstance(store.dataStores.dataStore, list) 

@pytest_mark.anyio
async def test_get_raster_stores_in_workspaces_no_store_fail(
    client: AsyncGeoServerX,
    httpx_mock: HTTPXMock,
    bad_coverages_stores_model_connection
):
    httpx_mock.add_response(json=bad_coverages_stores_model_connection)
    with pytest.raises(ValidationError):
        store = await client.get_raster_stores_in_workspaces('jay')

@pytest_mark.anyio
async def test_get_raster_stores_in_workspaces_success(
    client:AsyncGeoServerX,
    httpx_mock: HTTPXMock,
    good_coverages_stores_model_connection
):
    httpx_mock.add_response(json=good_coverages_stores_model_connection)
    store = await client.get_raster_stores_in_workspaces('cite')
    assert isinstance(store.coverageStores.coverageStore, list) 

@pytest_mark.anyio
async def test_allstyles_success(
    client:AsyncGeoServerX,
    httpx_mock: HTTPXMock,
    good_all_styles_model_connection
):
    httpx_mock.add_response(json=good_all_styles_model_connection)
    allstyles = await client.get_allstyles()
    assert isinstance(allstyles.styles.style, list) 

@pytest_mark.anyio
async def test_allstyles_fail(
    client:AsyncGeoServerX,
    httpx_mock: HTTPXMock,
    bad_all_styles_model_connection
):
    httpx_mock.add_response(json=bad_all_styles_model_connection)
    with pytest.raises(ValidationError):
        style = await client.get_allstyles()

@pytest_mark.anyio
async def test_style_success(
    client:AsyncGeoServerX,
    httpx_mock: HTTPXMock,
    good_style_model_connection
):
    httpx_mock.add_response(json=good_style_model_connection)
    style = await client.get_style('burg')
    assert style.style.name == 'burg'

@pytest_mark.anyio
async def test_style_fail(
    client:AsyncGeoServerX,
    httpx_mock: HTTPXMock,
    bad_style_model_connection
):
    httpx_mock.add_response(json=bad_style_model_connection)
    with pytest.raises(ValidationError):
        style = await client.get_style('dssdgsg')
