from enum import Enum
from geoserverx.models.gs_response import GSResponse


class GSResponseEnum(Enum):
    _404 = GSResponse(code=404, response="Result not found")
    _403 = GSResponse(code=403, response="Forbidden Request")
    _401 = GSResponse(code=401, response="Unauthorized request")
    _500 = GSResponse(code=500, response="Internal Server error")
    _201 = GSResponse(code=201, response="Data added successfully")
    _200 = GSResponse(code=200, response="Executed successfully")
    _204 = GSResponse(code=204, response="No Content")
    _400 = GSResponse(code=400, response="Bad Request")
    _409 = GSResponse(code=409, response="Same data found")
    _503 = GSResponse(code=503, response="Can't connect to Geoserver")


class HTTPXErrorEnum(Enum):
    runtime = "Client not found! Please check client parameters"
    requesterr = "Client Credentials are incorrect"
