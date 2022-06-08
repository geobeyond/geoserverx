import pytest

@pytest.fixture
def good_DataStoreInBulk_connection() -> dict :
    item = {"name":"just", "href":"https://www.linkedin.com/notifications/"}
    return item

@pytest.fixture
def bad_DataStoreInBulk_connection() -> dict :
    item = {"name":"just"}
    return item

@pytest.fixture
def good_DataStoreDict_connection() -> dict :
    item = {"dataStore": [
        {"name":"just", "href":"https://www.linkedin.com/notifications/"}
    ]}
    return item

@pytest.fixture
def bad_DataStoreDict_connection() -> dict :
    item = {"dataStore":''}
    return item

@pytest.fixture
def good_DatastoreConnection_connection() -> dict :
    item = {"key":"just", "path":"https://www.linkedin.com/notifications/"}
    
    return item

@pytest.fixture
def bad_DatastoreConnection_connection() -> dict :
    item = {"key":''}
    return item


@pytest.fixture
def good_EntryItem_connection() -> dict :
    item = {
        "entry": [
            {"key":"just", "path":"https://www.linkedin.com/notifications/"},
            {"key":"just", "path":"https://www.linkedin.com/notifications/"}
        ]
    }
    
    return item

@pytest.fixture
def bad_EntryItem_connection() -> dict :
    item = {"name":''}
    return item


@pytest.fixture
def good_DatastoreItem_connection() -> dict :
    item = {"name":"just", "connectionParameters":{
        "entry": [
            {"key":"just", "path":"https://www.linkedin.com/notifications/"},
            {"key":"just", "path":"https://www.linkedin.com/notifications/"}
        ]
    }}
    
    return item

@pytest.fixture
def bad_DatastoreItem_connection() -> dict :
    item = {"name":''}
    return item

@pytest.fixture
def good_DataStoreModel_connection() -> dict :
    item = {
    "dataStore": {
        "name": "jumper",
        "type": "Shapefile",
        "enabled": True,
        "workspace": {
            "name": "jaam",
            "href": "http://localhost:8080/geoserver/rest/workspaces/jaam.json"
        },
        "connectionParameters": {
            "entry": [
                {
                    "key": "namespace",
                    "path": "http://jaam"
                },
                {
                    "key": "url",
                    "path": "file:/usr/local/geoserver/bin/../data_dir/data/jaam/jumper/"
                }
            ]
        },
        "_default": False,
        "dateCreated": "2022-06-01 14:13:07.984 UTC",
        "dateModified": "2022-06-01 14:28:30.705 UTC",
        "featureTypes": "http://localhost:8080/geoserver/rest/workspaces/jaam/datastores/jumper/featuretypes.json"
    }
}
    
    return item

@pytest.fixture
def bad_DataStoreModel_connection() -> dict :
    item = {"dataStore":''}
    return item