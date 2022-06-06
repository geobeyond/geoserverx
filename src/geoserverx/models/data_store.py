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

class DatastoreConnection(BaseModel):
    key : str = Field(alias="@Key")
    path : str = Field(alias="$")

    class Config:
        allow_population_by_field_name = True

class EntryItem(BaseModel):
    entry : List[DatastoreConnection]

class DatastoreItem(BaseModel):
    name : str
    connectionParameters : EntryItem

class newDataStore(BaseModel):
    dataStore : DatastoreItem = {}


