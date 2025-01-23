from typing import List

from pydantic import BaseModel


class langVersion(BaseModel):
    version: str = ...


class SingleStyle(BaseModel):
    name: str = ...
    format: str = ...
    languageVersion: langVersion = ...
    filename: str = ...


class SingleStyleInList(BaseModel):
    name: str
    href: str


class AllStyleList(BaseModel):
    style: List[SingleStyleInList]
