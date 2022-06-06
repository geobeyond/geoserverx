from typing import Dict, List,Optional
from pydantic import BaseModel
from typing import Optional

from geoserverx.models.workspace import WorkspaceInBulk


class CoveragesStoreInBulk(BaseModel):
	name: str
	href: str


class CoveragesStoresDict(BaseModel):
	coverageStore: List[CoveragesStoreInBulk]


class CoveragesStoresModel(BaseModel):
	coverageStores:CoveragesStoresDict = {}


class CoveragesStoreModel(BaseModel):
	name: str
	description: str
	enabled: bool
	workspace: WorkspaceInBulk
	_default: bool
	url: str
	coverages: str
	dateCreated: str
	metadata: Optional[Dict] 
