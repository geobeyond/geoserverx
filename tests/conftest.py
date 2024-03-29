import pytest


@pytest.fixture
def good_workspaces_connection() -> dict:
    item = {
        "workspaces": {
            "workspace": [
                {
                    "name": "pydad",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/pydad.json",
                },
                {
                    "name": "jkzch",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/jkzch.json",
                },
                {
                    "name": "Pcqrv",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/Pcqrv.json",
                },
            ]
        }
    }
    return item


@pytest.fixture
def bad_workspaces_connection() -> dict:
    item = {"code": 502}
    return item


@pytest.fixture
def good_workspace_connection() -> dict:
    item = {
        "workspace": {
            "name": "pydad",
            "isolated": True,
            "dateCreated": "2022-06-04 07:55:31.903 UTC",
            "dataStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/datastores.json",
            "coverageStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/coveragestores.json",
            "wmsStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/wmsstores.json",
            "wmtsStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/wmtsstores.json",
        }
    }
    return item


@pytest.fixture
def bad_workspace_connection() -> dict:
    item = {"code": 404, "response": "Result not found"}
    return item


@pytest.fixture
def networkbad_workspace_connection() -> dict:
    item = {"code": 503, "response": "Geoserver unavailable"}
    return item


@pytest.fixture
def good_datastore_in_bulk_connection() -> dict:
    item = {"name": "just", "href": "https://www.linkedin.com/notifications/"}
    return item


@pytest.fixture
def bad_datastore_in_bulk_connection() -> dict:
    item = {"name": "just"}
    return item


@pytest.fixture
def good_datastore_dict_connection() -> dict:
    item = {
        "dataStore": [
            {"name": "just", "href": "https://www.linkedin.com/notifications/"}
        ]
    }
    return item


@pytest.fixture
def bad_datastore_dict_connection() -> dict:
    item = {"dataStore": ""}
    return item


@pytest.fixture
def good_datastores_model_connection() -> dict:
    item = {
        "dataStores": {
            "dataStore": [
                {
                    "name": "jumper",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/jaam/datastores/jumper.json",
                },
                {
                    "name": "nice",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/jaam/datastores/nice.json",
                },
                {
                    "name": "nyccc",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/jaam/datastores/nyccc.json",
                },
                {
                    "name": "resrrr",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/jaam/datastores/resrrr.json",
                },
            ]
        }
    }
    return item


@pytest.fixture
def bad_datastores_model_connection() -> dict:
    item = {"dataStores": "sd"}
    return item


@pytest.fixture
def invalid_datastores_model_connection() -> dict:
    item = {"code": 404, "response": "Result not found"}
    return item


@pytest.fixture
def good_datastore_connection_connection() -> dict:
    item = {"key": "just", "path": "https://www.linkedin.com/notifications/"}

    return item


@pytest.fixture
def bad_datastore_connection_connection() -> dict:
    item = {"key": ""}
    return item


@pytest.fixture
def good_entry_item_connection() -> dict:
    item = {
        "entry": [
            {"key": "just", "path": "https://www.linkedin.com/notifications/"},
            {"key": "just", "path": "https://www.linkedin.com/notifications/"},
        ]
    }

    return item


@pytest.fixture
def bad_entry_item_connection() -> dict:
    item = {"name": ""}
    return item


@pytest.fixture
def good_datastore_item_connection() -> dict:
    item = {
        "name": "just",
        "connectionParameters": {
            "entry": [
                {"key": "just", "path": "https://www.linkedin.com/notifications/"},
                {"key": "just", "path": "https://www.linkedin.com/notifications/"},
            ]
        },
    }

    return item


@pytest.fixture
def bad_datastore_item_connection() -> dict:
    item = {"dataStores": "abs"}
    return item


@pytest.fixture
def good_datastore_model_connection() -> dict:
    item = {
        "dataStore": {
            "name": "jumper",
            "type": "Shapefile",
            "enabled": True,
            "workspace": {
                "name": "jaam",
                "href": "http://localhost:8080/geoserver/rest/workspaces/jaam.json",
            },
            "connectionParameters": {
                "entry": [
                    {"key": "namespace", "path": "http://jaam"},
                    {
                        "key": "url",
                        "path": "file:/usr/local/geoserver/bin/../data_dir/data/jaam/jumper/",
                    },
                ]
            },
            "_default": False,
            "dateCreated": "2022-06-01 14:13:07.984 UTC",
            "dateModified": "2022-06-01 14:28:30.705 UTC",
            "featureTypes": "http://localhost:8080/geoserver/rest/workspaces/jaam/datastores/jumper/featuretypes.json",
        }
    }

    return item


@pytest.fixture
def bad_datastore_model_connection() -> dict:
    item = {"dataStore": ""}
    return item


@pytest.fixture
def invalid_datastore_model_connection() -> dict:
    item = {"code": 404, "response": "Result not found"}
    return item


@pytest.fixture
def good_coverages_store_in_bulk_connection() -> dict:
    item = {"name": "just", "href": "https://www.linkedin.com/notifications/"}
    return item


@pytest.fixture
def bad_coverages_store_in_bulk_connection() -> dict:
    item = {"name": "just"}
    return item


@pytest.fixture
def good_coverages_stores_dict_connection() -> dict:
    item = {
        "coverageStore": [
            {"name": "just", "href": "https://www.linkedin.com/notifications/"}
        ]
    }
    return item


@pytest.fixture
def bad_coverages_stores_dict_connection() -> dict:
    item = {"coverageStore": "just"}
    return item


@pytest.fixture
def good_coverages_stores_model_connection() -> dict:
    item = {
        "coverageStores": {
            "coverageStore": [
                {
                    "name": "RGB_125",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/cite/coveragestores/RGB_125.json",
                },
                {
                    "name": "kb",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/cite/coveragestores/kb.json",
                },
                {
                    "name": "nyc",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/cite/coveragestores/nyc.json",
                },
            ]
        }
    }
    return item


@pytest.fixture
def bad_coverages_stores_model_connection() -> dict:
    item = {"coverageStores": "just"}
    return item


@pytest.fixture
def invalid_coverages_stores_model_connection() -> dict:
    item = {"code": 404, "response": "Result not found"}
    return item


@pytest.fixture
def good_coverages_store_model_connection() -> dict:
    item = {
        "coverageStore": {
            "name": "RGB_125",
            "type": "GeoTIFF",
            "enabled": True,
            "workspace": {
                "name": "cite",
                "href": "http://localhost:8080/geoserver/rest/workspaces/cite.json",
            },
            "metadata": {
                "entry": {
                    "@key": "CogSettings.Key",
                    "cogSettings": {
                        "useCachingStream": False,
                        "rangeReaderSettings": "HTTP",
                    },
                }
            },
            "_default": False,
            "dateCreated": "2022-05-13 17:46:26.336 UTC",
            "url": "cog://https://khetiimagery.s3.amazonaws.com/farm_ndvi/2022-05-05/0013f18b-3aeb-4ae3-804b-514818f98940.tif",
            "coverages": "http://localhost:8080/geoserver/rest/workspaces/cite/coveragestores/RGB_125/coverages.json",
        }
    }
    return item


@pytest.fixture
def bad_coverages_store_model_connection() -> dict:
    item = {"coverageStores": "just"}
    return item


@pytest.fixture
def invalid_coverages_store_model_connection() -> dict:
    item = {"code": 404, "response": "Result not found"}
    return item


@pytest.fixture
def good_single_style_dict_connection() -> dict:
    item = {
        "name": "burg",
        "format": "sld",
        "languageVersion": {"version": "1.0.0"},
        "filename": "burg.sld",
    }
    return item


@pytest.fixture
def bad_single_style_dict_connection() -> dict:
    item = {"name": ""}
    return item


@pytest.fixture
def good_style_model_connection() -> dict:
    item = {
        "style": {
            "name": "burg",
            "format": "sld",
            "languageVersion": {"version": "1.0.0"},
            "filename": "burg.sld",
        }
    }
    return item


@pytest.fixture
def bad_style_model_connection() -> dict:
    item = {"style": ""}
    return item


@pytest.fixture
def invalid_style_model_connection() -> dict:
    item = {"code": 404, "response": "Result not found"}
    return item


@pytest.fixture
def good_all_style_list_connection() -> dict:
    item = {
        "name": "CUSD 2020 Census Blocks",
        "href": "http://localhost:8080/geoserver/rest/styles/CUSD+2020+Census+Blocks.json",
    }
    return item


@pytest.fixture
def bad_all_style_list_connection() -> dict:
    item = {"name": ""}
    return item


@pytest.fixture
def good_all_style_dict_connection() -> dict:
    item = {
        "style": [
            {
                "name": "CUSD 2020 Census Blocks",
                "href": "http://localhost:8080/geoserver/rest/styles/CUSD+2020+Census+Blocks.json",
            },
            {
                "name": "Default Styler",
                "href": "http://localhost:8080/geoserver/rest/styles/Default+Styler.json",
            },
        ]
    }
    return item


@pytest.fixture
def bad_all_style_dict_connection() -> dict:
    item = {"style": ""}
    return item


@pytest.fixture
def good_all_styles_model_connection() -> dict:
    item = {
        "styles": {
            "style": [
                {
                    "name": "CUSD 2020 Census Blocks",
                    "href": "http://localhost:8080/geoserver/rest/styles/CUSD+2020+Census+Blocks.json",
                },
                {
                    "name": "Default Styler",
                    "href": "http://localhost:8080/geoserver/rest/styles/Default+Styler.json",
                },
            ]
        }
    }
    return item


@pytest.fixture
def bad_all_styles_model_connection() -> dict:
    item = {"styles": ""}
    return item


@pytest.fixture
def invalid_all_styles_model_connection() -> dict:
    item = {"code": 404, "response": "Result not found"}
    return item


@pytest.fixture
def good_workspace_in_bulk_connection() -> dict:
    item = {
        "name": "pydad",
        "href": "http://localhost:8080/geoserver/rest/workspaces/pydad.json",
    }
    return item


@pytest.fixture
def bad_workspace_in_bulk_connection() -> dict:
    item = {"name": ""}
    return item


@pytest.fixture
def good_workspace_dict_connection() -> dict:
    item = {
        "workspace": [
            {
                "name": "pydad",
                "href": "http://localhost:8080/geoserver/rest/workspaces/pydad.json",
            },
            {
                "name": "jkzch",
                "href": "http://localhost:8080/geoserver/rest/workspaces/jkzch.json",
            },
        ]
    }
    return item


@pytest.fixture
def bad_workspace_dict_connection() -> dict:
    item = {"workspace": ""}
    return item


@pytest.fixture
def good_workspaces_model_connection() -> dict:
    item = {
        "workspaces": {
            "workspace": [
                {
                    "name": "pydad",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/pydad.json",
                },
                {
                    "name": "jkzch",
                    "href": "http://localhost:8080/geoserver/rest/workspaces/jkzch.json",
                },
            ]
        }
    }
    return item


@pytest.fixture
def bad_workspaces_model_connection() -> dict:
    item = {"workspaces": ""}
    return item


@pytest.fixture
def good_workspace_model_connection() -> dict:
    item = {
        "workspace": {
            "name": "pydad",
            "isolated": True,
            "dateCreated": "2022-06-04 07:55:31.903 UTC",
            "dataStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/datastores.json",
            "coverageStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/coveragestores.json",
            "wmsStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/wmsstores.json",
            "wmtsStores": "http://localhost:8080/geoserver/rest/workspaces/pydad/wmtsstores.json",
        }
    }
    return item


@pytest.fixture
def bad_workspace_model_connection() -> dict:
    item = {"workspace": ""}
    return item


@pytest.fixture
def good_new_workspace_connection() -> dict:
    item = {"workspace": {"name": "pydad", "isolated": True}}
    return item


@pytest.fixture
def bad_new_workspace_connection() -> dict:
    item = {"workspace": ""}
    return item


@pytest.fixture
def invalid_new_workspace_connection() -> dict:
    item = {"code": 404, "response": "Result not found"}
    return item


@pytest.fixture
def bad_new_pg_store_connection() -> dict:
    item = {"store": ""}
    return item


@pytest.fixture
def invalid_new_pg_store_connection() -> dict:
    item = {"code": 404, "response": "Result not found"}
    return item


@pytest.fixture
def good_new_pg_store_connection() -> dict:
    item = {
        "dataStore": {
            "name": "pgg",
            "connectionParameters": {
                "host": "localhost",
                "port": 5432,
                "database": "postgres",
                "user": "postgres",
                "passwd": "postgres",
                "dbtype": "postgis",
            },
        }
    }
    return item


@pytest.fixture
def good_layers_connection() -> dict:
    item = {
        "layers": {
            "layer": [
                {
                    "name": "tiger:giant_polygon",
                    "href": "http://localhost:8080/geoserver/rest/layers/tiger%3Agiant_polygon.json",
                },
                {
                    "name": "tiger:poi",
                    "href": "http://localhost:8080/geoserver/rest/layers/tiger%3Apoi.json",
                },
                {
                    "name": "tiger:poly_landmarks",
                    "href": "http://localhost:8080/geoserver/rest/layers/tiger%3Apoly_landmarks.json",
                },
            ]
        }
    }
    return item


@pytest.fixture
def bad_layers_connection() -> dict:
    item = {"code": 502}
    return item


@pytest.fixture
def good_layer_connection() -> dict:
    item = {
        "layer": {
            "name": "poi",
            "path": "/",
            "type": "VECTOR",
            "defaultStyle": {
                "name": "poi",
                "href": "http://localhost:8080/geoserver/rest/styles/poi.json",
            },
            "styles": {
                "@class": "linked-hash-set",
                "style": [
                    {
                        "name": "burg",
                        "href": "http://localhost:8080/geoserver/rest/styles/burg.json",
                    },
                    {
                        "name": "point",
                        "href": "http://localhost:8080/geoserver/rest/styles/point.json",
                    },
                ],
            },
            "resource": {
                "@class": "featureType",
                "name": "tiger:poi",
                "href": "http://localhost:8080/geoserver/rest/workspaces/tiger/datastores/nyc/featuretypes/poi.json",
            },
            "attribution": {"logoWidth": 0, "logoHeight": 0},
        }
    }
    return item


@pytest.fixture
def bad_layer_connection() -> dict:
    item = {"code": 404, "response": "Result not found"}
    return item


@pytest.fixture
def networkbad_layer_connection() -> dict:
    item = {"code": 503, "response": "Geoserver unavailable"}
    return item
