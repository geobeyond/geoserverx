from typing import List
from pydantic import BaseModel


class WorkspaceInBulk(BaseModel):
    name: str
    href: str


class workspaceDict(BaseModel):
    workspaces: List[WorkspaceInBulk]

class WorkspacesModel(BaseModel):
    workspaces = workspaceDict


class WorkspaceModel(BaseModel):
    name: str
    isolated: bool
    dateCreated: str
    dataStores: str
    coverageStores: str
    wmsStores: str
    wmtsStores: str


class NewWorkspaceInfo(BaseModel):
    name :str
    isolated:bool

class NewWorkspace(BaseModel):
    workspace : NewWorkspaceInfo