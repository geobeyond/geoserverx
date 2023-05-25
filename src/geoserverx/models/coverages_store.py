from typing import Dict, List, Optional, Union, Literal
from pydantic import BaseModel

from geoserverx.models.workspace import WorkspaceInBulk


class CoveragesStoreInBulk(BaseModel):
    name: str = ...
    href: str = ...


class CoveragesStoresDict(BaseModel):
    coverageStore: List[CoveragesStoreInBulk] = ...


class CoveragesStoresModel(BaseModel):
    coverageStores: Union[CoveragesStoresDict, Literal[""]] = ""


class CoveragesStoreModelDetail(BaseModel):
    name: str = ...
    description: str = None
    enabled: bool = ...
    workspace: WorkspaceInBulk = ...
    _default: bool = ...
    url: str = ...
    coverages: str = ...
    dateCreated: Optional[str]
    metadata: Optional[Dict] = None


class CoveragesStoreModel(BaseModel):
    coverageStore: CoveragesStoreModelDetail
