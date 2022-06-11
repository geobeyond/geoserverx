from pytest import fixture, mark as pytest_mark
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


# @pytest_mark.anyio
# def test_workspace_success(client:SyncGeoServerX):
#     worksp = client.get_workspace('df')
#     assert worksp.workspace.name == 'df'

# @pytest_mark.anyio
# def test_workspace_fail(client:SyncGeoServerX):
#     worksp = client.get_workspace('sfsf')
#     assert worksp.code == 404

# # @pytest_mark.anyio
# # def test_create_workspace_fail(client:SyncGeoServerX):
# #     try:
# #         worksp = client.create_workspace(x)
# #         assert False
# #     except :
# #         assert True

# # @pytest_mark.anyio
# # def test_create_workspace_fail(client:SyncGeoServerX):
# #     try :
# #         worksp = client.create_workspace()
# #         assert False
# #     except : 
# #         assert True


# @pytest_mark.anyio
# def test_create_workspace_duplicate_fail(client:SyncGeoServerX):
#     worksp = client.create_workspace('ad')
#     assert worksp.code == 409

# @pytest_mark.anyio
# def test_create_workspace_success(client:SyncGeoServerX):
#     letters = string.ascii_letters
#     x = "".join(random.sample(letters,5))   
#     worksp = client.create_workspace(x)
#     assert worksp.code == 201


# @pytest_mark.anyio
# def test_get_vector_stores_in_workspaces_no_ws_fail(client:SyncGeoServerX):
#     store = client.get_vector_stores_in_workspaces('cisfte')
#     assert store.code == 404


# @pytest_mark.anyio
# def test_get_vector_stores_in_workspaces_no_store_fail(client:SyncGeoServerX):
#     store = client.get_vector_stores_in_workspaces('cite')
#     assert store.dataStores == ""

# @pytest_mark.anyio
# def test_get_vector_stores_in_workspaces_success(client:SyncGeoServerX):
#     store = client.get_vector_stores_in_workspaces('jaam')
#     assert isinstance(store.dataStores.dataStore, list) 



# @pytest_mark.anyio
# def test_get_raster_stores_in_workspaces_no_ws_fail(client:SyncGeoServerX):
#     store = client.get_raster_stores_in_workspaces('cisfte')
#     assert store.code == 404

# @pytest_mark.anyio
# def test_get_raster_stores_in_workspaces_no_store_fail(client:SyncGeoServerX):
#     store = client.get_raster_stores_in_workspaces('jay')
#     assert store.coverageStores == ""

# @pytest_mark.anyio
# def test_get_raster_stores_in_workspaces_success(client:SyncGeoServerX):
#     store = client.get_raster_stores_in_workspaces('cite')
#     assert isinstance(store.coverageStores.coverageStore, list) 


# @pytest_mark.anyio
# def test_allstyles_success(client:SyncGeoServerX):
#     allstyles = client.get_allstyles()
#     assert isinstance(allstyles.styles.style, list) 

# @pytest_mark.anyio
# def test_style_success(client:SyncGeoServerX):
#     style = client.get_style('generic')
#     assert style.style.name == 'generic'

# @pytest_mark.anyio
# def test_style_fail(client:SyncGeoServerX):
#     style = client.get_style('dssdgsg')
#     assert style.code == 404