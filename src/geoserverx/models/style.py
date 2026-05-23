from typing import List

from pydantic import BaseModel


class LangVersion(BaseModel):
    version: str = ...


class SingleStyle(BaseModel):
    name: str = ...
    format: str = ...
    languageVersion: LangVersion = ...
    filename: str = ...


class StyleModel(BaseModel):
    style: SingleStyle


class AllStyleList(BaseModel):
    name: str
    href: str


class AllStyle(BaseModel):
    style: List[AllStyleList]


class AllStylesModel(BaseModel):
    styles: AllStyle
