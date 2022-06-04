from typing import List
from pydantic import BaseModel, Field

from .workspace import WorkspaceInBulk


class DataStoreInBulk(BaseModel):
    name: str
    href: str


class DataStores(BaseModel):
    dataStores = {"dataStore": List[DataStoreInBulk]}


class DataStore(BaseModel):
    name: str
    description: str
    enabled: bool
    workspace: WorkspaceInBulk
    connectionParameters: dict
    _default: bool
    dateCreated: str
    dateModified: str
    featureTypes: str

class datastore_connection_param_dict(BaseModel):
    key : str = Field(alias="@Key")
    path : str = Field(alias="$")


class datastore_connection_param(BaseModel):
    entry : List[datastore_connection_param_dict]

class datastoreDetail(BaseModel):
    name : str
    connectionParameters : datastore_connection_param

class newDataStore(BaseModel):
    dataStore : datastoreDetail = {}


