import pytest,asyncio
from GeoServerX.src.geoserverx.Utils.auth import GeoServerXAuth
from GeoServerX.src.geoserverx._Async.gsx import AsyncGeoServerX
from GeoServerX.src.geoserverx._Sync.gsx import SyncGeoServerX



def test_get_workspace(url, username, password):
    print("-------------start-----------------")
    print(f"testing start for - {url}")
    client = SyncGeoServerX(username, password,url)
    # print(client.get_all_workspaces())
    # print(client.get_raster_stores_in_workspaces('nurc'))
    # print(client.get_store_information('rastsder','cite','nyc'))
    # print(client.get_allstyles())
    print(client.get_styles('tiger_roads'))
    print(f"testing done for - {url}")
    print("-------------end-----------------")

test_get_workspace(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver')


@pytest.mark.asyncio
async def as_test_get_workspace(url, username, password):
    client = AsyncGeoServerX(username, password,url)
    print("-------------start-----------------")
    res = await client.get_all_workspaces()
    print(res)
    print("-------------end-----------------")
    res = await client.get_workspaces('df')
    print(res)
    print("-------------end-----------------")

# asyncio.run(as_test_get_workspace(url='http://localhost:8080/geoserver/rest/',username='admin', password='geoserver'))
