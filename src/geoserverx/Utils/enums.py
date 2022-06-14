from enum import Enum
from geoserverx.models.gs_response import GSResponse


class GSResponseEnum(Enum):
    _404 = GSResponse(code=404, response="Result not found")
    _401 = GSResponse(code=401, response="Unauthorized request")
    _500 = GSResponse(code=500, response="Internal Server error")
    _201 = GSResponse(code=201, response="Data added successfully")
    _409 = GSResponse(code=409, response="Same data found")