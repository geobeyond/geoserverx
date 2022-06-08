import pytest
from pydantic import ValidationError
from geoserverx import SyncGeoServerX, GeoServerXAuth,GeoServerXError
from geoserverx.models.data_store import DataStoreInBulk,DataStoreDict,DatastoreConnection,EntryItem,DatastoreItem,DataStoreModel,DataStoresModel
from geoserverx.models.coverages_store import CoveragesStoreInBulk,CoveragesStoreModel,CoveragesStoresDict,CoveragesStoresModel
from geoserverx.models.style import SingleStyleDict,StyleModel,allStyleList,allStyleDict,AllStylesModel
from geoserverx.models.workspace import WorkspaceInBulk,workspaceDict,WorkspaceModel,WorkspacesModel,NewWorkspace,NewWorkspaceInfo,SingleWorkspace
''' ------ DataStore testing ------ '''
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

# Testing DataStoresModel
def test_DataStoresModel_connection(good_DataStoresModel_connection):
    ds_connection = DataStoresModel(**good_DataStoresModel_connection)
    assert ds_connection.dataStores.dataStore[0].name == "jumper"

def test_DataStoresModel_failure(bad_DataStoresModel_connection):
    with pytest.raises(ValidationError):
        ds_connection = DataStoresModel(**bad_DataStoresModel_connection)


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
    assert ds_connection.dataStore.name == "jumper"

def test_DataStoreModel_failure(bad_DataStoreModel_connection):
    with pytest.raises(ValidationError):
        ds_connection = DataStoreModel(**bad_DataStoreModel_connection)


''' ------ CoveragesStore testing ------ '''
# Testing CoveragesStoreInBulk
def test_CoveragesStoreInBulk_connection(good_CoveragesStoreInBulk_connection):
    ds_connection = CoveragesStoreInBulk(**good_CoveragesStoreInBulk_connection)
    assert ds_connection.name == "just"
    assert ds_connection.href == "https://www.linkedin.com/notifications/"

def test_CoveragesStoreInBulk_failure(bad_CoveragesStoreInBulk_connection):
    with pytest.raises(ValidationError):
        ds_connection = CoveragesStoreInBulk(**bad_CoveragesStoreInBulk_connection)

# Testing CoveragesStoresDict
def test_CoveragesStoresDict_connection(good_CoveragesStoresDict_connection):
    ds_connection = CoveragesStoresDict(**good_CoveragesStoresDict_connection)
    assert ds_connection.coverageStore[0].name == "just"

def test_CoveragesStoresDict_failure(bad_CoveragesStoresDict_connection):
    with pytest.raises(ValidationError):
        ds_connection = CoveragesStoresDict(**bad_CoveragesStoresDict_connection)


# Testing CoveragesStoresModel
def test_CoveragesStoresModel_connection(good_CoveragesStoresModel_connection):
    ds_connection = CoveragesStoresModel(**good_CoveragesStoresModel_connection)
    assert ds_connection.coverageStores.coverageStore[0].name == "RGB_125"

def test_CoveragesStoresModel_failure(bad_CoveragesStoresModel_connection):
    with pytest.raises(ValidationError):
        ds_connection = CoveragesStoresModel(**bad_CoveragesStoresModel_connection)


# Testing CoveragesStoreModel
def test_CoveragesStoreModel_connection(good_CoveragesStoreModel_connection):
    ds_connection = CoveragesStoreModel(**good_CoveragesStoreModel_connection)
    assert ds_connection.coverageStore.name == "RGB_125"

def test_CoveragesStoreModel_failure(bad_CoveragesStoreModel_connection):
    with pytest.raises(ValidationError):
        ds_connection = CoveragesStoreModel(**bad_CoveragesStoreModel_connection)

''' ------ Style testing ------ '''
# Testing SingleStyleDict
def test_SingleStyleDict_connection(good_SingleStyleDict_connection):
    ds_connection = SingleStyleDict(**good_SingleStyleDict_connection)
    assert ds_connection.name == "burg"

def test_SingleStyleDict_failure(bad_SingleStyleDict_connection):
    with pytest.raises(ValidationError):
        ds_connection = SingleStyleDict(**bad_SingleStyleDict_connection)

# Testing StyleModel
def test_StyleModel_connection(good_StyleModel_connection):
    ds_connection = StyleModel(**good_StyleModel_connection)
    assert ds_connection.style.name == "burg"

def test_StyleModel_failure(bad_StyleModel_connection):
    with pytest.raises(ValidationError):
        ds_connection = StyleModel(**bad_StyleModel_connection)

# Testing allStyleList
def test_allStyleList_connection(good_allStyleList_connection):
    ds_connection = allStyleList(**good_allStyleList_connection)
    assert ds_connection.name == "CUSD 2020 Census Blocks"

def test_allStyleList_failure(bad_allStyleList_connection):
    with pytest.raises(ValidationError):
        ds_connection = allStyleList(**bad_allStyleList_connection)

# Testing allStyleDict
def test_allStyleDict_connection(good_allStyleDict_connection):
    ds_connection = allStyleDict(**good_allStyleDict_connection)
    assert ds_connection.style[0].name == "CUSD 2020 Census Blocks"

def test_allStyleDict_failure(bad_allStyleDict_connection):
    with pytest.raises(ValidationError):
        ds_connection = allStyleDict(**bad_allStyleDict_connection)

# Testing AllStylesModel
def test_AllStylesModel_connection(good_AllStylesModel_connection):
    ds_connection = AllStylesModel(**good_AllStylesModel_connection)
    assert ds_connection.styles.style[0].name == "CUSD 2020 Census Blocks"

def test_AllStylesModel_failure(bad_AllStylesModel_connection):
    with pytest.raises(ValidationError):
        ds_connection = AllStylesModel(**bad_AllStylesModel_connection)

''' ------ Workspace testing ------ '''
# Testing WorkspaceInBulk
def test_WorkspaceInBulk_connection(good_WorkspaceInBulk_connection):
    ds_connection = WorkspaceInBulk(**good_WorkspaceInBulk_connection)
    assert ds_connection.name == "pydad"

def test_WorkspaceInBulk_failure(bad_WorkspaceInBulk_connection):
    with pytest.raises(ValidationError):
        ds_connection = WorkspaceInBulk(**bad_WorkspaceInBulk_connection)

# Testing workspaceDict
def test_workspaceDict_connection(good_workspaceDict_connection):
    ds_connection = workspaceDict(**good_workspaceDict_connection)
    assert ds_connection.workspace[0].name == "pydad"

def test_workspaceDict_failure(bad_workspaceDict_connection):
    with pytest.raises(ValidationError):
        ds_connection = workspaceDict(**bad_workspaceDict_connection)

# Testing WorkspacesModel
def test_WorkspacesModel_connection(good_WorkspacesModel_connection):
    ds_connection = WorkspacesModel(**good_WorkspacesModel_connection)
    assert ds_connection.workspaces.workspace[0].name == "pydad"

def test_WorkspacesModel_failure(bad_WorkspacesModel_connection):
    with pytest.raises(ValidationError):
        ds_connection = WorkspacesModel(**bad_WorkspacesModel_connection)

# Testing WorkspaceModel
def test_WorkspaceModel_connection(good_WorkspaceModel_connection):
    ds_connection = WorkspaceModel(**good_WorkspaceModel_connection)
    assert ds_connection.workspace.name == "pydad"

def test_WorkspaceModel_failure(bad_WorkspaceModel_connection):
    with pytest.raises(ValidationError):
        ds_connection = WorkspaceModel(**bad_WorkspaceModel_connection)

# Testing NewWorkspace
def test_NewWorkspace_connection(good_NewWorkspace_connection):
    ds_connection = NewWorkspace(**good_NewWorkspace_connection)
    assert ds_connection.workspace.name == "pydad"

def test_NewWorkspace_failure(bad_NewWorkspace_connection):
    with pytest.raises(ValidationError):
        ds_connection = NewWorkspace(**bad_NewWorkspace_connection)
