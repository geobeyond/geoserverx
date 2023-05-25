from typing import List
from pydantic import BaseModel


class langVersion(BaseModel):
    version: str = ...


class SingleStyleDict(BaseModel):
    name: str = ...
    format: str = ...
    languageVersion: langVersion = ...
    filename: str = ...


class StyleModel(BaseModel):
    style: SingleStyleDict


class allStyleList(BaseModel):
    name: str
    href: str


class allStyleDict(BaseModel):
    style: List[allStyleList]


class AllStylesModel(BaseModel):
    styles: allStyleDict
