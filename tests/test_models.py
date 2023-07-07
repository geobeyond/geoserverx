import pytest
from pydantic import ValidationError

from geoserverx.models.coverages_store import (CoveragesStoreInBulk,
                                               CoveragesStoreModel,
                                               CoveragesStoresDict,
                                               CoveragesStoresModel)
from geoserverx.models.data_store import (DatastoreConnection, DataStoreDict,
                                          DataStoreInBulk, DatastoreItem,
                                          DataStoreModel, DataStoresModel,
                                          EntryItem)
from geoserverx.models.layer_group import (LayerGroupsModel,
                                           SingleLayerGroupModel)
from geoserverx.models.style import (AllStylesModel, SingleStyleDict,
                                     StyleModel, allStyleDict, allStyleList)
from geoserverx.models.workspace import (NewWorkspace, NewWorkspaceInfo,
                                         SingleWorkspace, WorkspaceInBulk,
                                         WorkspaceModel, WorkspacesModel,
                                         workspaceDict)


# Testing DataStoreInBulk
def test_DataStoreInBulk_connection(good_datastore_in_bulk_connection):
    ds_connection = DataStoreInBulk(**good_datastore_in_bulk_connection)
    assert ds_connection.name == "just"
    assert ds_connection.href == "https://www.linkedin.com/notifications/"


def test_DataStoreInBulk_failure(bad_datastore_in_bulk_connection):
    with pytest.raises(ValidationError):
        ds_connection = DataStoreInBulk(**bad_datastore_in_bulk_connection)


# Testing DataStoreDict
def test_DataStoreDict_connection(good_datastore_dict_connection):
    ds_connection = DataStoreDict(**good_datastore_dict_connection)
    assert ds_connection.dataStore[0].name == "just"


def test_DataStoreDict_failure(bad_datastore_dict_connection):
    with pytest.raises(ValidationError):
        ds_connection = DataStoreDict(**bad_datastore_dict_connection)


# Testing DataStoresModel
def test_DataStoresModel_connection(good_datastores_model_connection):
    ds_connection = DataStoresModel(**good_datastores_model_connection)
    assert ds_connection.dataStores.dataStore[0].name == "jumper"


def test_DataStoresModel_failure(bad_datastores_model_connection):
    with pytest.raises(ValidationError):
        ds_connection = DataStoresModel(**bad_datastores_model_connection)


# Testing DatastoreConnection
def test_DatastoreConnection_connection(good_datastore_connection_connection):
    ds_connection = DatastoreConnection(**good_datastore_connection_connection)
    assert ds_connection.key == "just"


def test_DatastoreConnection_failure(bad_datastore_connection_connection):
    with pytest.raises(ValidationError):
        ds_connection = DatastoreConnection(**bad_datastore_connection_connection)


# Testing EntryItem
def test_EntryItem_connection(good_entry_item_connection):
    ds_connection = EntryItem(**good_entry_item_connection)
    assert ds_connection.entry[0].key == "just"


def test_EntryItem_failure(bad_entry_item_connection):
    with pytest.raises(ValidationError):
        ds_connection = EntryItem(**bad_entry_item_connection)


# Testing DatastoreItem
def test_DatastoreItem_connection(good_datastore_item_connection):
    ds_connection = DatastoreItem(**good_datastore_item_connection)
    assert ds_connection.connectionParameters.entry[0].key == "just"


def test_DatastoreItem_failure(bad_datastore_item_connection):
    with pytest.raises(ValidationError):
        ds_connection = DatastoreItem(**bad_datastore_item_connection)


# Testing DataStoreModel
def test_DataStoreModel_connection(good_datastore_model_connection):
    ds_connection = DataStoreModel(**good_datastore_model_connection)
    assert ds_connection.dataStore.name == "jumper"


def test_DataStoreModel_failure(bad_datastore_model_connection):
    with pytest.raises(ValidationError):
        ds_connection = DataStoreModel(**bad_datastore_model_connection)


# Testing CoveragesStoreInBulk
def test_CoveragesStoreInBulk_connection(good_coverages_store_in_bulk_connection):
    ds_connection = CoveragesStoreInBulk(**good_coverages_store_in_bulk_connection)
    assert ds_connection.name == "just"
    assert ds_connection.href == "https://www.linkedin.com/notifications/"


def test_CoveragesStoreInBulk_failure(bad_coverages_store_in_bulk_connection):
    with pytest.raises(ValidationError):
        ds_connection = CoveragesStoreInBulk(**bad_coverages_store_in_bulk_connection)


# Testing CoveragesStoresDict
def test_CoveragesStoresDict_connection(good_coverages_stores_dict_connection):
    ds_connection = CoveragesStoresDict(**good_coverages_stores_dict_connection)
    assert ds_connection.coverageStore[0].name == "just"


def test_CoveragesStoresDict_failure(bad_coverages_stores_dict_connection):
    with pytest.raises(ValidationError):
        ds_connection = CoveragesStoresDict(**bad_coverages_stores_dict_connection)


# Testing CoveragesStoresModel
def test_CoveragesStoresModel_connection(good_coverages_stores_model_connection):
    ds_connection = CoveragesStoresModel(**good_coverages_stores_model_connection)
    assert ds_connection.coverageStores.coverageStore[0].name == "RGB_125"


def test_CoveragesStoresModel_failure(bad_coverages_stores_model_connection):
    with pytest.raises(ValidationError):
        ds_connection = CoveragesStoresModel(**bad_coverages_stores_model_connection)


# Testing CoveragesStoreModel
def test_CoveragesStoreModel_connection(good_coverages_store_model_connection):
    ds_connection = CoveragesStoreModel(**good_coverages_store_model_connection)
    assert ds_connection.coverageStore.name == "RGB_125"


def test_CoveragesStoreModel_failure(bad_coverages_store_model_connection):
    with pytest.raises(ValidationError):
        ds_connection = CoveragesStoreModel(**bad_coverages_store_model_connection)


# Testing SingleStyleDict
def test_SingleStyleDict_connection(good_single_style_dict_connection):
    ds_connection = SingleStyleDict(**good_single_style_dict_connection)
    assert ds_connection.name == "burg"


def test_SingleStyleDict_failure(bad_single_style_dict_connection):
    with pytest.raises(ValidationError):
        ds_connection = SingleStyleDict(**bad_single_style_dict_connection)


# Testing StyleModel
def test_StyleModel_connection(good_style_model_connection):
    ds_connection = StyleModel(**good_style_model_connection)
    assert ds_connection.style.name == "burg"


def test_StyleModel_failure(bad_style_model_connection):
    with pytest.raises(ValidationError):
        ds_connection = StyleModel(**bad_style_model_connection)


# Testing allStyleList
def test_allStyleList_connection(good_all_style_list_connection):
    ds_connection = allStyleList(**good_all_style_list_connection)
    assert ds_connection.name == "CUSD 2020 Census Blocks"


def test_allStyleList_failure(bad_all_style_list_connection):
    with pytest.raises(ValidationError):
        ds_connection = allStyleList(**bad_all_style_list_connection)


# Testing allStyleDict
def test_allStyleDict_connection(good_all_style_dict_connection):
    ds_connection = allStyleDict(**good_all_style_dict_connection)
    assert ds_connection.style[0].name == "CUSD 2020 Census Blocks"


def test_allStyleDict_failure(bad_all_style_dict_connection):
    with pytest.raises(ValidationError):
        ds_connection = allStyleDict(**bad_all_style_dict_connection)


# Testing AllStylesModel
def test_AllStylesModel_connection(good_all_styles_model_connection):
    ds_connection = AllStylesModel(**good_all_styles_model_connection)
    assert ds_connection.styles.style[0].name == "CUSD 2020 Census Blocks"


def test_AllStylesModel_failure(bad_all_styles_model_connection):
    with pytest.raises(ValidationError):
        ds_connection = AllStylesModel(**bad_all_styles_model_connection)


# Testing WorkspaceInBulk
def test_WorkspaceInBulk_connection(good_workspace_in_bulk_connection):
    ds_connection = WorkspaceInBulk(**good_workspace_in_bulk_connection)
    assert ds_connection.name == "pydad"


def test_WorkspaceInBulk_failure(bad_workspace_in_bulk_connection):
    with pytest.raises(ValidationError):
        ds_connection = WorkspaceInBulk(**bad_workspace_in_bulk_connection)


# Testing workspaceDict
def test_workspaceDict_connection(good_workspace_dict_connection):
    ds_connection = workspaceDict(**good_workspace_dict_connection)
    assert ds_connection.workspace[0].name == "pydad"


def test_workspaceDict_failure(bad_workspace_dict_connection):
    with pytest.raises(ValidationError):
        ds_connection = workspaceDict(**bad_workspace_dict_connection)


# Testing WorkspacesModel
def test_WorkspacesModel_connection(good_workspaces_model_connection):
    ds_connection = WorkspacesModel(**good_workspaces_model_connection)
    assert ds_connection.workspaces.workspace[0].name == "pydad"


def test_WorkspacesModel_failure(bad_workspaces_model_connection):
    with pytest.raises(ValidationError):
        ds_connection = WorkspacesModel(**bad_workspaces_model_connection)


# Testing WorkspaceModel
def test_WorkspaceModel_connection(good_workspace_model_connection):
    ds_connection = WorkspaceModel(**good_workspace_model_connection)
    assert ds_connection.workspace.name == "pydad"


def test_WorkspaceModel_failure(bad_workspace_model_connection):
    with pytest.raises(ValidationError):
        ds_connection = WorkspaceModel(**bad_workspace_model_connection)


# Testing NewWorkspace
def test_NewWorkspace_connection(good_new_workspace_connection):
    ds_connection = NewWorkspace(**good_new_workspace_connection)
    assert ds_connection.workspace.name == "pydad"


def test_NewWorkspace_failure(bad_new_workspace_connection):
    with pytest.raises(ValidationError):
        ds_connection = NewWorkspace(**bad_new_workspace_connection)


# all layer groups
def test_LayerGroupsModel_connection(good_all_layer_group_connection):
    ds_connection = LayerGroupsModel(**good_all_layer_group_connection)
    assert ds_connection.layerGroups.layerGroup[0].name == "a"


def test_LayerGroupsModel_failure(bad_all_layer_group_connection):
    with pytest.raises(ValidationError):
        ds_connection = LayerGroupsModel(**bad_all_layer_group_connection)


# single layer group
def test_SingleLayerGroupModel_connection(good_layer_group_connection):
    ds_connection = SingleLayerGroupModel(**good_layer_group_connection)
    assert ds_connection.layerGroup.name == "a"


def test_SingleLayerGroupModel_failure(bad_layer_group_connection):
    with pytest.raises(ValidationError):
        ds_connection = SingleLayerGroupModel(**bad_layer_group_connection)
