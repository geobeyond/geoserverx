from typing import List, Literal, Optional

from pydantic import BaseModel


class Attribute(BaseModel):
    name: str
    dataType: str
    accessType: str


class LayerDetails(BaseModel):
    layerType: Optional[str] = None
    defaultStyle: Optional[str] = None
    cqlFilterRead: Optional[str] = None
    cqlFilterWrite: Optional[str] = None
    allowedArea: Optional[str] = None
    spatialFilterType: Optional[str] = None
    catalogMode: Optional[str] = None
    allowedStyles: List[str] = []
    attributes: List[Attribute]


class Rule(BaseModel):
    priority: int
    userName: Optional[str] = None
    roleName: Optional[str] = None
    addressRange: Optional[str] = None
    workspace: Optional[str] = None
    layer: Optional[str] = None
    service: Optional[Literal["GWC", "WMS", "WCS", "WFS"]] = None
    request: Optional[str] = None
    subfield: Optional[str] = None
    access: Literal["ALLOW", "DENY", "LIMIT"] = "ALLOW"
    limits: Optional[str] = None
    layerDetails: Optional[LayerDetails] = None


class GetRule(Rule):
    id: Optional[int] = None


class RulesResponse(BaseModel):
    count: int
    rules: List[GetRule]


class NewRule(BaseModel):
    Rule: Rule
