import pytest
from pydantic import ValidationError
from geoserverx import SyncGeoServerX, GeoServerXAuth,GeoServerXError
from geoserverx.models.data_store import DataStoreInBulk,DataStoreDict,DatastoreConnection,EntryItem,DatastoreItem,newDataStore,DataStoreModel


# Testing DataStoreInBulk
def test_DataStoreInBulk_connection(good_DataStoreInBulk_connection):
    ds_connection = DataStoreInBulk(**good_DataStoreInBulk_connection)
    assert ds_connection.name == "just"
    assert ds_connection.href == "https://www.linkedin.com/notifications/"

def test_DataStoreInBulk_failure(bad_DataStoreInBulk_connection):
    with pytest.raises(ValidationError):
        ds_connection = DataStoreInBulk(**bad_DataStoreInBulk_connection)

# Testing DataStoreDict
def test_DataStoreDict_connection(good_DataStoreDict_connection):
    ds_connection = DataStoreDict(**good_DataStoreDict_connection)
    assert ds_connection.dataStore[0].name == "just"

def test_DataStoreDict_failure(bad_DataStoreDict_connection):
    with pytest.raises(ValidationError):
        ds_connection = DataStoreDict(**bad_DataStoreDict_connection)

# Testing DatastoreConnection
def test_DatastoreConnection_connection(good_DatastoreConnection_connection):
    ds_connection = DatastoreConnection(**good_DatastoreConnection_connection)
    assert ds_connection.key == "just"

def test_DatastoreConnection_failure(bad_DatastoreConnection_connection):
    with pytest.raises(ValidationError):
        ds_connection = DatastoreConnection(**bad_DatastoreConnection_connection)

# Testing EntryItem
def test_EntryItem_connection(good_EntryItem_connection):
    ds_connection = EntryItem(**good_EntryItem_connection)
    assert ds_connection.entry[0].key == "just"

def test_EntryItem_failure(bad_EntryItem_connection):
    with pytest.raises(ValidationError):
        ds_connection = EntryItem(**bad_EntryItem_connection)

# Testing DatastoreItem
def test_DatastoreItem_connection(good_DatastoreItem_connection):
    ds_connection = DatastoreItem(**good_DatastoreItem_connection)
    assert ds_connection.connectionParameters.entry[0].key == "just"

def test_DatastoreItem_failure(bad_DatastoreItem_connection):
    with pytest.raises(ValidationError):
        ds_connection = DatastoreItem(**bad_DatastoreItem_connection)


# Testing DataStoreModel
def test_DataStoreModel_connection(good_DataStoreModel_connection):
    ds_connection = DataStoreModel(**good_DataStoreModel_connection)
    assert ds_connection.name == "just"

def test_DataStoreModel_failure(bad_DataStoreModel_connection):
    with pytest.raises(ValidationError):
        ds_connection = DataStoreModel(**bad_DataStoreModel_connection)
