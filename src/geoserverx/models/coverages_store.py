from typing import Dict, List
from pydantic import BaseModel
from pyparsing import Optional

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
    connectionParameters: Optional[Dict] 
    _default: bool
    url: str
    coverages: str
    dateCreated: str
    metadata:Optional[Dict] 
