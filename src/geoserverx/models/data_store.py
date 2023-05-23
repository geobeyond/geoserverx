from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field

from .workspace import WorkspaceInBulk


class DataStoreInBulk(BaseModel):
    name: str = ...
    href: str = ...


class DataStoreDict(BaseModel):
    dataStore: List[DataStoreInBulk]


class DataStoresModel(BaseModel):
    dataStores: Union[DataStoreDict, Literal[""]] = ""


class DatastoreConnection(BaseModel):
    key: str = Field(..., alias="@key")
    path: str = Field(..., alias="$")

    class Config:
        allow_population_by_field_name = True


class EntryItem(BaseModel):
    entry: List[DatastoreConnection]


class DatastoreItem(BaseModel):
    name: str
    connectionParameters: EntryItem


class DataStoreModelDetails(BaseModel):
    name: str = ...
    description: str = None
    enabled: bool = ...
    workspace: WorkspaceInBulk = ...
    connectionParameters: EntryItem = ...
    _default: bool = ...
    dateCreated: Optional[str]
    dateModified: Optional[str]
    featureTypes: str


class DataStoreModel(BaseModel):
    dataStore: DataStoreModelDetails = {}


class CreateStoreItem(BaseModel):
    host: str
    port: int
    database: str
    user: str
    passwd: str
    dbtype: str


class CreateDataStoreModel(BaseModel):
    name: str
    connectionParameters: CreateStoreItem


class MainCreateDataStoreModel(BaseModel):
    dataStore: CreateDataStoreModel
