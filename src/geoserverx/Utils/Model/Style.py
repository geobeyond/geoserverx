from typing import List
from pydantic import BaseModel


class Style(BaseModel):
    code: int
    name: str
    format: str
    languageVersion: dict
    filename: str
