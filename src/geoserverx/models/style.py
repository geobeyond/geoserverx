from typing import List

from pydantic import BaseModel


class langVersion(BaseModel):
    version: str = ...


class SingleStyle(BaseModel):
    name: str = ...
    format: str = ...
    languageVersion: langVersion = ...
    filename: str = ...


class StyleModel(BaseModel):
    style: SingleStyle


class allStyleList(BaseModel):
    name: str
    href: str


class allStyle(BaseModel):
    style: List[allStyleList]


class AllStylesModel(BaseModel):
    styles: allStyle
