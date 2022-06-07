from typing import Dict, List,Optional, Union
from pydantic import BaseModel

from .workspace import WorkspaceInBulk
# from . import WorkspaceInBulk


class CoveragesStoreInBulk(BaseModel):
	name: str
	href: str

class CoveragesStoresDict(BaseModel):
	coverageStore: List[CoveragesStoreInBulk]

class CoveragesStoresModel(BaseModel):
	coverageStores: Union[CoveragesStoresDict, str] = ''

class CoveragesStoreModel(BaseModel):
	name: str
	description: str
	enabled: bool
	workspace: WorkspaceInBulk
	_default: bool
	url: str
	coverages: str
	dateCreated: str
	metadata:Optional[Dict] 
