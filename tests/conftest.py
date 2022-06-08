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
def good_DataStoresModel_connection() -> dict :
    item = {
    "dataStores": {
        "dataStore": [
            {
                "name": "jumper",
                "href": "http://localhost:8080/geoserver/rest/workspaces/jaam/datastores/jumper.json"
            },
            {
                "name": "nice",
                "href": "http://localhost:8080/geoserver/rest/workspaces/jaam/datastores/nice.json"
            },
            {
                "name": "nyccc",
                "href": "http://localhost:8080/geoserver/rest/workspaces/jaam/datastores/nyccc.json"
            },
            {
                "name": "resrrr",
                "href": "http://localhost:8080/geoserver/rest/workspaces/jaam/datastores/resrrr.json"
            }
        ]
    }
}
    return item

@pytest.fixture
def bad_DataStoresModel_connection() -> dict :
    item = {"dataStores":''}
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

@pytest.fixture
def good_CoveragesStoreInBulk_connection() -> dict :
    item = {"name":"just", "href":"https://www.linkedin.com/notifications/"}
    return item

@pytest.fixture
def bad_CoveragesStoreInBulk_connection() -> dict :
    item = {"name":"just"}
    return item

@pytest.fixture
def good_CoveragesStoresDict_connection() -> dict :
    item = {"coverageStore":[
        {"name":"just", "href":"https://www.linkedin.com/notifications/"}
        ]}
    return item

@pytest.fixture
def bad_CoveragesStoresDict_connection() -> dict :
    item = {"coverageStore":"just"}
    return item

@pytest.fixture
def good_CoveragesStoresModel_connection() -> dict :
    item ={
    "coverageStores": {
        "coverageStore": [
            {
                "name": "RGB_125",
                "href": "http://localhost:8080/geoserver/rest/workspaces/cite/coveragestores/RGB_125.json"
            },
            {
                "name": "kb",
                "href": "http://localhost:8080/geoserver/rest/workspaces/cite/coveragestores/kb.json"
            },
            {
                "name": "nyc",
                "href": "http://localhost:8080/geoserver/rest/workspaces/cite/coveragestores/nyc.json"
            }
        ]
    }
}
    return item

@pytest.fixture
def bad_CoveragesStoresModel_connection() -> dict :
    item = {"coverageStores":"just"}
    return item


@pytest.fixture
def good_CoveragesStoreModel_connection() -> dict :
    item ={
    "coverageStore": {
        "name": "RGB_125",
        "type": "GeoTIFF",
        "enabled": True,
        "workspace": {
            "name": "cite",
            "href": "http://localhost:8080/geoserver/rest/workspaces/cite.json"
        },
        "metadata": {
            "entry": {
                "@key": "CogSettings.Key",
                "cogSettings": {
                    "useCachingStream": False,
                    "rangeReaderSettings": "HTTP"
                }
            }
        },
        "_default": False,
        "dateCreated": "2022-05-13 17:46:26.336 UTC",
        "url": "cog://https://khetiimagery.s3.amazonaws.com/farm_ndvi/2022-05-05/0013f18b-3aeb-4ae3-804b-514818f98940.tif",
        "coverages": "http://localhost:8080/geoserver/rest/workspaces/cite/coveragestores/RGB_125/coverages.json"
    }
}
    return item

@pytest.fixture
def bad_CoveragesStoreModel_connection() -> dict :
    item = {"coverageStores":"just"}
    return item



@pytest.fixture
def good_SingleStyleDict_connection() -> dict :
    item = {
        "name": "burg",
        "format": "sld",
        "languageVersion": {
            "version": "1.0.0"
        },
        "filename": "burg.sld"
    }
    return item

@pytest.fixture
def bad_SingleStyleDict_connection() -> dict :
    item = {"name":""}
    return item

@pytest.fixture
def good_StyleModel_connection() -> dict :
    item = {
    "style": {
        "name": "burg",
        "format": "sld",
        "languageVersion": {
            "version": "1.0.0"
        },
        "filename": "burg.sld"
    }
}
    return item

@pytest.fixture
def bad_StyleModel_connection() -> dict :
    item = {"style":""}
    return item


@pytest.fixture
def good_allStyleList_connection() -> dict :
    item =  {
                "name": "CUSD 2020 Census Blocks",
                "href": "http://localhost:8080/geoserver/rest/styles/CUSD+2020+Census+Blocks.json"
            }
    return item

@pytest.fixture
def bad_allStyleList_connection() -> dict :
    item = {"name":""}
    return item



@pytest.fixture
def good_allStyleDict_connection() -> dict :
    item = {"style": [
            {
                "name": "CUSD 2020 Census Blocks",
                "href": "http://localhost:8080/geoserver/rest/styles/CUSD+2020+Census+Blocks.json"
            },
            {
                "name": "Default Styler",
                "href": "http://localhost:8080/geoserver/rest/styles/Default+Styler.json"
            }
        ]
    }
    return item

@pytest.fixture
def bad_allStyleDict_connection() -> dict :
    item = {"style":""}
    return item


@pytest.fixture
def good_AllStylesModel_connection() -> dict :
    item = {"styles":{"style": [
            {
                "name": "CUSD 2020 Census Blocks",
                "href": "http://localhost:8080/geoserver/rest/styles/CUSD+2020+Census+Blocks.json"
            },
            {
                "name": "Default Styler",
                "href": "http://localhost:8080/geoserver/rest/styles/Default+Styler.json"
            }
        ]
    }}
    return item

@pytest.fixture
def bad_AllStylesModel_connection() -> dict :
    item = {"styles":""}
    return item


@pytest.fixture
def good_WorkspaceInBulk_connection() -> dict :
    item = {
                "name": "pydad",
                "href": "http://localhost:8080/geoserver/rest/workspaces/pydad.json"
            }
    return item

@pytest.fixture
def bad_WorkspaceInBulk_connection() -> dict :
    item = {"name":""}
    return item


@pytest.fixture
def good_workspaceDict_connection() -> dict :
    item = {"workspace": [
            {
                "name": "pydad",
                "href": "http://localhost:8080/geoserver/rest/workspaces/pydad.json"
            },
            {
                "name": "jkzch",
                "href": "http://localhost:8080/geoserver/rest/workspaces/jkzch.json"
            }]}
    return item

@pytest.fixture
def bad_workspaceDict_connection() -> dict :
    item = {"workspace":""}
    return item

@pytest.fixture
def good_WorkspacesModel_connection() -> dict :
    item = {"workspaces":{"workspace": [
            {
                "name": "pydad",
                "href": "http://localhost:8080/geoserver/rest/workspaces/pydad.json"
            },
            {
                "name": "jkzch",
                "href": "http://localhost:8080/geoserver/rest/workspaces/jkzch.json"
            }]}}
    return item

@pytest.fixture
def bad_WorkspacesModel_connection() -> dict :
    item = {"workspaces":""}
    return item


@pytest.fixture
def good_WorkspaceModel_connection() -> dict :
    item = {
    "workspace": {
        "name": "pydad",
        "isolated": True,
        "dateCreated": "2022-06-04 07:55:31.903 UTC",
        "dataStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/datastores.json",
        "coverageStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/coveragestores.json",
        "wmsStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/wmsstores.json",
        "wmtsStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/wmtsstores.json"
    }
}
    return item

@pytest.fixture
def bad_WorkspaceModel_connection() -> dict :
    item = {"workspace":""}
    return item

@pytest.fixture
def good_NewWorkspace_connection() -> dict :
    item = {
    "workspace": {
        "name": "pydad",
        "isolated": True
    }
}
    return item

@pytest.fixture
def bad_NewWorkspace_connection() -> dict :
    item = {"workspace":""}
    return item
