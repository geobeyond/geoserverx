from geoserverx import SyncGeoServerX, GeoServerXAuth,GeoServerXError

from pytest import fixture, mark as pytest_mark




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
def test_all_workspaces(client:SyncGeoServerX):
    allwork = client.get_all_workspaces()
    assert allwork.workspaces.workspace[0].name


@pytest_mark.anyio
def test_workspace_success(client:SyncGeoServerX):
    worksp = client.get_workspace('df')
    assert worksp.workspace.name

@pytest_mark.anyio
def test_workspace_fail(client:SyncGeoServerX):
    worksp = client.get_workspace('sfsf')
    assert worksp.response

@pytest_mark.anyio
def test_create_workspace_fail(client:SyncGeoServerX):
    try:
        worksp = client.create_workspace()
        assert False
    except :
        assert True

@pytest_mark.anyio
def test_create_workspace_success(client:SyncGeoServerX):
    worksp = client.create_workspace('gym')
    assert worksp.response
