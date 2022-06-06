from enum import Enum


class GSResponse(Enum):
    _404 = {"code" : 404,"error":"Result not found"}
    _401 = {"code" : 401,"error":"Unauthorized request"}
    _500 = {"code" : 500,"error":"Internal Server error"}
    _201 = {"code" : 201,"error":"Data added successfully"}
    _409 = {"code" : 409,"error":"Same data found"}