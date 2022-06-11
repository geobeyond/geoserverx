from pydantic import BaseModel


class GSResponse(BaseModel):
    code: int
    response : str
