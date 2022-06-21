from pydantic import BaseModel


class GSResponse(BaseModel):
    code: int
    response : str

class HttpxError(BaseModel):
    response : str