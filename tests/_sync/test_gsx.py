from pydantic import ValidationError
from pytest import fixture, mark as pytest_mark
import pytest
from pytest_httpx import HTTPXMock
from geoserverx.models.workspace import WorkspaceInBulk
from geoserverx._sync.gsx import (
    SyncGeoServerX, GeoServerXAuth, GeoServerXError
)


@fixture(name="client")
def create_client():
    client = SyncGeoServerX.from_auth(GeoServerXAuth())
    yield client
    client.close()

@pytest_mark.anyio
def test_error():
    try:
        client = SyncGeoServerX(url="",username="",password="")
        assert False
    except GeoServerXError:
        assert True


@pytest_mark.anyio
def test_all_workspaces(client:SyncGeoServerX,httpx_mock: HTTPXMock,good_Workspaces_connection):
    httpx_mock.add_response(json=good_Workspaces_connection)
    allwork = client.get_all_workspaces()
    if len(allwork.workspaces.workspace) > 0:
        assert isinstance(allwork.workspaces.workspace[0], WorkspaceInBulk)
    else :
        assert isinstance(allwork.workspaces.workspace, list) 


@pytest_mark.anyio
def test_workspace_success(client:SyncGeoServerX,httpx_mock: HTTPXMock,good_Workspace_connection):
    httpx_mock.add_response(json=good_Workspace_connection)
    worksp = client.get_workspace('pydad')
    assert worksp.workspace.name == 'pydad'

@pytest_mark.anyio
def test_workspace_fail(client:SyncGeoServerX,httpx_mock: HTTPXMock,bad_Workspace_connection):
    httpx_mock.add_response(json=bad_Workspace_connection)
    with pytest.raises(ValidationError):
        worksp = client.get_workspace('sfsf')

@pytest_mark.anyio
def test_get_vector_stores_in_workspaces_no_ws_fail(client:SyncGeoServerX,httpx_mock: HTTPXMock,bad_DatastoreItem_connection):
    httpx_mock.add_response(json=bad_DatastoreItem_connection)
    with pytest.raises(ValidationError):
        store = client.get_vector_stores_in_workspaces('cisfte')

@pytest_mark.anyio
def test_get_vector_stores_in_workspaces_success(client:SyncGeoServerX,httpx_mock: HTTPXMock,good_DataStoresModel_connection):
    httpx_mock.add_response(json=good_DataStoresModel_connection)
    store = client.get_vector_stores_in_workspaces('jn')
    assert isinstance(store.dataStores.dataStore, list) 


@pytest_mark.anyio
def test_get_raster_stores_in_workspaces_no_store_fail(client:SyncGeoServerX,httpx_mock: HTTPXMock,bad_CoveragesStoresModel_connection):
    httpx_mock.add_response(json=bad_CoveragesStoresModel_connection)
    with pytest.raises(ValidationError):
        store = client.get_raster_stores_in_workspaces('jay')

@pytest_mark.anyio
def test_get_raster_stores_in_workspaces_success(client:SyncGeoServerX,httpx_mock: HTTPXMock,good_CoveragesStoresModel_connection):
    httpx_mock.add_response(json=good_CoveragesStoresModel_connection)
    store = client.get_raster_stores_in_workspaces('cite')
    assert isinstance(store.coverageStores.coverageStore, list) 


@pytest_mark.anyio
def test_allstyles_success(client:SyncGeoServerX,httpx_mock: HTTPXMock,good_AllStylesModel_connection):
    httpx_mock.add_response(json=good_AllStylesModel_connection)
    allstyles = client.get_allstyles()
    assert isinstance(allstyles.styles.style, list) 

@pytest_mark.anyio
def test_allstyles_fail(client:SyncGeoServerX,httpx_mock: HTTPXMock,bad_AllStylesModel_connection):
    httpx_mock.add_response(json=bad_AllStylesModel_connection)
    with pytest.raises(ValidationError):
        style = client.get_allstyles()

@pytest_mark.anyio
def test_style_success(client:SyncGeoServerX,httpx_mock: HTTPXMock,good_StyleModel_connection):
    httpx_mock.add_response(json=good_StyleModel_connection)
    style = client.get_style('burg')
    assert style.style.name == 'burg'

@pytest_mark.anyio
def test_style_fail(client:SyncGeoServerX,httpx_mock: HTTPXMock,bad_StyleModel_connection):
    httpx_mock.add_response(json=bad_StyleModel_connection)
    with pytest.raises(ValidationError):
        style = client.get_style('dssdgsg')
