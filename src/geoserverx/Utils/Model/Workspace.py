from typing import List
from pydantic import BaseModel


class WorkspaceInBulk(BaseModel):
    name: str
    href: str


class workspaceDict(BaseModel):
    workspaces: List[WorkspaceInBulk]

class Workspaces(BaseModel):
    workspaces = workspaceDict


class Workspace(BaseModel):
    name: str
    isolated: bool
    dateCreated: str
    dataStores: str
    coverageStores: str
    wmsStores: str
    wmtsStores: str


class addWorkspaceDetails(BaseModel):
    name :str
    isolated:bool

class addWorkspace(BaseModel):
    workspace : addWorkspaceDetails