from typing import List
from pydantic import BaseModel

from .workspace import WorkspaceInBulk


class CoveragesStoreInBulk(BaseModel):
    name: str
    href: str


class CoveragesStores(BaseModel):
    coverageStores:dict = {"coverageStore": List[CoveragesStoreInBulk]}

class CovergesStoreList(BaseModel):
    __root__ : CoveragesStoreInBulk = {}

class CoveragesStore(BaseModel):
    name: str
    description: str
    enabled: bool
    workspace: WorkspaceInBulk
    connectionParameters: dict
    _default: bool
    url: str
    coverages: str
    dateCreated: str
