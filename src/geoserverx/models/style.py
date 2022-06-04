from typing import List
from pydantic import BaseModel


class Style(BaseModel):
    code: int
    name: str
    format: str
    languageVersion: dict
    filename: str

class allStyleLise(BaseModel):
    name : str
    href : str

class allStyleDict(BaseModel):
    style : List[allStyleLise]

class allStyles(BaseModel):
    styles : allStyleDict