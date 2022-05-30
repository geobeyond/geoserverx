import pytest
from pytest import mark as pytest_mark


from geoserverx import AsyncGeoServerX

url='http://localhost:8080/geoserver/rest/'
username='admin'
password='geoserver'

@pytest_mark.anyio
async def as_test_get_workspace(url, username, password):
    print("-------------start-----------------")
    print(f"testing start for - {url}")
    client = AsyncGeoServerX(username, password,url)
    response = await client.get_all_workspaces()
    assert response.status_code == 201