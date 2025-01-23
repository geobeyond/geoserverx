from typing import List, Optional

from pydantic import BaseModel


class WorkspaceInBulk(BaseModel):
    name: str = ...
    href: str = ...


class workspaceDict(BaseModel):
    workspace: List[WorkspaceInBulk]


class SingleWorkspace(BaseModel):
    name: str = ...
    isolated: bool = ...
    dateCreated: Optional[str] = None
    dataStores: str = ...
    coverageStores: str = ...
    wmsStores: str = ...
    wmtsStores: str = ...


class WorkspaceModel(BaseModel):
    workspace: SingleWorkspace = ...


class UpdateWorkspaceInfo(BaseModel):
    name: Optional[str] = None
    isolated: Optional[bool] = None
