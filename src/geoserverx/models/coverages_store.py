from typing import List
from pydantic import BaseModel

from .workspace import WorkspaceInBulk
# from . import WorkspaceInBulk


class CoveragesStoreInBulk(BaseModel):
    name: str
    href: str

class CoveragesStoresDict(BaseModel):
    coverageStore: List[CoveragesStoreInBulk]

class CoveragesStoresModel(BaseModel):
    coverageStores = CoveragesStoresDict

class CoveragesStoreModel(BaseModel):
    name: str
    description: str
    enabled: bool
    workspace: WorkspaceInBulk
    connectionParameters: dict
    _default: bool
    url: str
    coverages: str
    dateCreated: str
