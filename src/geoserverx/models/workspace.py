from typing import List, Optional
from pydantic import BaseModel


class WorkspaceInBulk(BaseModel):
    name: str = ...
    href: str = ...


class workspaceDict(BaseModel):
    workspace: List[WorkspaceInBulk]


class WorkspacesModel(BaseModel):
    workspaces: workspaceDict = ""


class SingleWorkspace(BaseModel):
    name: str = ...
    isolated: bool = ...
    dateCreated: Optional[str]
    dataStores: str = ...
    coverageStores: str = ...
    wmsStores: str = ...
    wmtsStores: str = ...


class WorkspaceModel(BaseModel):
    workspace: SingleWorkspace = ...


class NewWorkspaceInfo(BaseModel):
    name: str = ...
    isolated: bool = None


class NewWorkspace(BaseModel):
    workspace: NewWorkspaceInfo = ...
