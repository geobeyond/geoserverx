from typing import List, Optional, Union
from pydantic import BaseModel, Field

from .workspace import WorkspaceInBulk


class DataStoreInBulk(BaseModel):
    name: str = ...
    href: str = ...

class DataStoreDict(BaseModel):
    dataStore: List[DataStoreInBulk]

class DataStoresModel(BaseModel):
    dataStores: Union[DataStoreDict, str] = ''



class DatastoreConnection(BaseModel):
    key : str = Field(...,alias="@Key")
    path : str = Field(...,alias="$")

    class Config:
        allow_population_by_field_name = True

class EntryItem(BaseModel):
    entry : List[DatastoreConnection]

class DatastoreItem(BaseModel):
    name : str
    connectionParameters : EntryItem


class DataStoreModelDetails(BaseModel):
    name: str = ...
    description: str = None
    enabled: bool = ...
    workspace: WorkspaceInBulk = ...
    connectionParameters: EntryItem = ...
    _default: bool = ...
    dateCreated: str
    dateModified: str
    featureTypes: str


class DataStoreModel(BaseModel):
    dataStore : DataStoreModelDetails = {}

