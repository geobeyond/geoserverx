from typing import Optional
from pydantic import BaseModel


class GSResponse(BaseModel):
    code: Optional[int]
    response: str = ...


class HttpxError(BaseModel):
    response: str
