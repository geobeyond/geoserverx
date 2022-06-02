from typing import List
from pydantic import BaseModel


class WorkspaceInBulk(BaseModel):
    name: str
    href: str


class Workspaces(BaseModel):
    workspaces = {"workspaces": List[WorkspaceInBulk]}


class Workspace(BaseModel):
    name: str
    isolated: bool
    dateCreated: str
    dataStores: str
    coverageStores: str
    wmsStores: str
    wmtsStores: str
