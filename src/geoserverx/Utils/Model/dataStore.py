from typing import List
from pydantic import BaseModel

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
