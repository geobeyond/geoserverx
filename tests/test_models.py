import pytest
from pydantic import ValidationError

from geoserverx.models.coverages_store import (
    CoveragesStoreInBulk,
    CoveragesStoreModel,
    CoveragesStoresDict,
    CoveragesStoresModel,
)
from geoserverx.models.data_store import (
    DatastoreConnection,
    DataStoreDict,
    DataStoreInBulk,
    DatastoreItem,
    DataStoreModel,
    DataStoresModel,
    EntryItem,
)
from geoserverx.models.geofence import RulesResponse
from geoserverx.models.layer_group import LayerGroupsModel
from geoserverx.models.style import (
    AllStylesModel,
    SingleStyle,
    StyleModel,
    allStyle,
    allStyleList,
)
from geoserverx.models.workspace import (
    NewWorkspace,
    WorkspaceInBulk,
    WorkspaceModel,
    WorkspacesModel,
    workspaceDict,
)


# Testing DataStoreInBulk
def test_datastoreinbulk_connection(good_datastore_in_bulk_connection):
    ds_connection = DataStoreInBulk(**good_datastore_in_bulk_connection)
    assert ds_connection.name == "just"
    assert ds_connection.href == "https://www.linkedin.com/notifications/"


def test_datastoreinbulk_failure(bad_datastore_in_bulk_connection):
    with pytest.raises(ValidationError):
        DataStoreInBulk(**bad_datastore_in_bulk_connection)


# Testing DataStoreDict
def test_datastoredict_connection(good_datastore_dict_connection):
    ds_connection = DataStoreDict(**good_datastore_dict_connection)
    assert ds_connection.dataStore[0].name == "just"


def test_datastoredict_failure(bad_datastore_dict_connection):
    with pytest.raises(ValidationError):
        DataStoreDict(**bad_datastore_dict_connection)


# Testing DataStoresModel
def test_datastoresmodel_connection(good_datastores_model_connection):
    ds_connection = DataStoresModel(**good_datastores_model_connection)
    assert ds_connection.dataStores.dataStore[0].name == "jumper"


def test_datastoresmodel_failure(bad_datastores_model_connection):
    with pytest.raises(ValidationError):
        DataStoresModel(**bad_datastores_model_connection)


# Testing DatastoreConnection
def test_datastoreconnection_connection(good_datastore_connection_connection):
    ds_connection = DatastoreConnection(**good_datastore_connection_connection)
    assert ds_connection.key == "just"


def test_datastoreconnection_failure(bad_datastore_connection_connection):
    with pytest.raises(ValidationError):
        DatastoreConnection(**bad_datastore_connection_connection)


# Testing EntryItem
def test_entryitem_connection(good_entry_item_connection):
    ds_connection = EntryItem(**good_entry_item_connection)
    assert ds_connection.entry[0].key == "just"


def test_entryitem_failure(bad_entry_item_connection):
    with pytest.raises(ValidationError):
        EntryItem(**bad_entry_item_connection)


# Testing DatastoreItem
def test_datastoreitem_connection(good_datastore_item_connection):
    ds_connection = DatastoreItem(**good_datastore_item_connection)
    assert ds_connection.connectionParameters.entry[0].key == "just"


def test_datastoreitem_failure(bad_datastore_item_connection):
    with pytest.raises(ValidationError):
        DatastoreItem(**bad_datastore_item_connection)


# Testing DataStoreModel
def test_datastoremodel_connection(good_datastore_model_connection):
    ds_connection = DataStoreModel(**good_datastore_model_connection)
    assert ds_connection.dataStore.name == "jumper"


def test_datastoremodel_failure(bad_datastore_model_connection):
    with pytest.raises(ValidationError):
        DataStoreModel(**bad_datastore_model_connection)


# Testing CoveragesStoreInBulk
def test_coveragesstoreinbulk_connection(good_coverages_store_in_bulk_connection):
    ds_connection = CoveragesStoreInBulk(**good_coverages_store_in_bulk_connection)
    assert ds_connection.name == "just"
    assert ds_connection.href == "https://www.linkedin.com/notifications/"


def test_coveragesstoreinbulk_failure(bad_coverages_store_in_bulk_connection):
    with pytest.raises(ValidationError):
        CoveragesStoreInBulk(**bad_coverages_store_in_bulk_connection)


# Testing CoveragesStoresDict
def test_coveragesstoresdict_connection(good_coverages_stores_dict_connection):
    ds_connection = CoveragesStoresDict(**good_coverages_stores_dict_connection)
    assert ds_connection.coverageStore[0].name == "just"


def test_coveragesstoresdict_failure(bad_coverages_stores_dict_connection):
    with pytest.raises(ValidationError):
        CoveragesStoresDict(**bad_coverages_stores_dict_connection)


# Testing CoveragesStoresModel
def test_coveragesstoresmodel_connection(good_coverages_stores_model_connection):
    ds_connection = CoveragesStoresModel(**good_coverages_stores_model_connection)
    assert ds_connection.coverageStores.coverageStore[0].name == "RGB_125"


def test_coveragesstoresmodel_failure(bad_coverages_stores_model_connection):
    with pytest.raises(ValidationError):
        CoveragesStoresModel(**bad_coverages_stores_model_connection)


# Testing CoveragesStoreModel
def test_coveragesstoremodel_connection(good_coverages_store_model_connection):
    ds_connection = CoveragesStoreModel(**good_coverages_store_model_connection)
    assert ds_connection.coverageStore.name == "RGB_125"


def test_coveragesstoremodel_failure(bad_coverages_store_model_connection):
    with pytest.raises(ValidationError):
        CoveragesStoreModel(**bad_coverages_store_model_connection)


# Testing SingleStyle
def test_singlestyle_connection(good_single_style_dict_connection):
    ds_connection = SingleStyle(**good_single_style_dict_connection)
    assert ds_connection.name == "burg"


def test_singlestyle_failure(bad_single_style_dict_connection):
    with pytest.raises(ValidationError):
        SingleStyle(**bad_single_style_dict_connection)


# Testing StyleModel
def test_stylemodel_connection(good_style_model_connection):
    ds_connection = StyleModel(**good_style_model_connection)
    assert ds_connection.style.name == "burg"


def test_stylemodel_failure(bad_style_model_connection):
    with pytest.raises(ValidationError):
        StyleModel(**bad_style_model_connection)


# Testing allStyleList
def test_allstylelist_connection(good_all_style_list_connection):
    ds_connection = allStyleList(**good_all_style_list_connection)
    assert ds_connection.name == "CUSD 2020 Census Blocks"


def test_allstylelist_failure(bad_all_style_list_connection):
    with pytest.raises(ValidationError):
        allStyleList(**bad_all_style_list_connection)


# Testing allStyle
def test_allstyle_connection(good_all_style_dict_connection):
    ds_connection = allStyle(**good_all_style_dict_connection)
    assert ds_connection.style[0].name == "CUSD 2020 Census Blocks"


def test_allstyle_failure(bad_all_style_dict_connection):
    with pytest.raises(ValidationError):
        allStyle(**bad_all_style_dict_connection)


# Testing AllStylesModel
def test_allstylesmodel_connection(good_all_styles_model_connection):
    ds_connection = AllStylesModel(**good_all_styles_model_connection)
    assert ds_connection.styles.style[0].name == "CUSD 2020 Census Blocks"


def test_allstylesmodel_failure(bad_all_styles_model_connection):
    with pytest.raises(ValidationError):
        AllStylesModel(**bad_all_styles_model_connection)


# Testing WorkspaceInBulk
def test_workspaceinbulk_connection(good_workspace_in_bulk_connection):
    ds_connection = WorkspaceInBulk(**good_workspace_in_bulk_connection)
    assert ds_connection.name == "pydad"


def test_workspaceinbulk_failure(bad_workspace_in_bulk_connection):
    with pytest.raises(ValidationError):
        WorkspaceInBulk(**bad_workspace_in_bulk_connection)


# Testing workspaceDict
def test_workspacedict_connection(good_workspace_dict_connection):
    ds_connection = workspaceDict(**good_workspace_dict_connection)
    assert ds_connection.workspace[0].name == "pydad"


def test_workspacedict_failure(bad_workspace_dict_connection):
    with pytest.raises(ValidationError):
        workspaceDict(**bad_workspace_dict_connection)


# Testing WorkspacesModel
def test_workspacesmodel_connection(good_workspaces_model_connection):
    ds_connection = WorkspacesModel(**good_workspaces_model_connection)
    assert ds_connection.workspaces.workspace[0].name == "pydad"


def test_workspacesmodel_failure(bad_workspaces_model_connection):
    with pytest.raises(ValidationError):
        WorkspacesModel(**bad_workspaces_model_connection)


# Testing WorkspaceModel
def test_workspacemodel_connection(good_workspace_model_connection):
    ds_connection = WorkspaceModel(**good_workspace_model_connection)
    assert ds_connection.workspace.name == "pydad"


def test_workspacemodel_failure(bad_workspace_model_connection):
    with pytest.raises(ValidationError):
        WorkspaceModel(**bad_workspace_model_connection)


# Testing NewWorkspace
def test_newworkspace_connection(good_new_workspace_connection):
    ds_connection = NewWorkspace(**good_new_workspace_connection)
    assert ds_connection.workspace.name == "pydad"


def test_newworkspace_failure(bad_new_workspace_connection):
    with pytest.raises(ValidationError):
        NewWorkspace(**bad_new_workspace_connection)


# Testing LayerGroupsModel
def test_layergroupsmodel_connection(good_layer_groups_connection):
    ds_connection = LayerGroupsModel(**good_layer_groups_connection)
    assert ds_connection.layerGroups.layerGroup[0].name == "tg"


def test_layergroupsmodel_failure(bad_layer_groups_connection):
    with pytest.raises(ValidationError):
        LayerGroupsModel(**bad_layer_groups_connection)


# Testing LayerGroupsModel
def test_RulesResponse_connection(good_all_geofence_rules_connection):
    ds_connection = RulesResponse(**good_all_geofence_rules_connection)
    assert ds_connection.count == 2


def test_RulesResponse_failure(bad_all_geofence_rules_connection):
    with pytest.raises(ValidationError):
        RulesResponse(**bad_all_geofence_rules_connection)
