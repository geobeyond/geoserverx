from pydantic import BaseModel
from typing import List, Optional

class Attribute(BaseModel):
    name: str
    dataType: str
    accessType: str

class LayerDetails(BaseModel):
    layerType: str
    defaultStyle: Optional[str] = None
    cqlFilterRead: Optional[str] = None
    cqlFilterWrite: Optional[str] = None
    allowedArea: Optional[str] = None
    spatialFilterType: Optional[str] = None
    catalogMode: Optional[str] = None
    allowedStyles: List[str] = []
    attributes: List[Attribute]

class Rule(BaseModel):
    id: int
    priority: int
    userName: Optional[str] = None
    roleName: str
    addressRange: Optional[str] = None
    workspace: str
    layer: str
    service: Optional[str] = None
    request: Optional[str] = None
    subfield: Optional[str] = None
    access: str
    limits: Optional[str] = None
    layerDetails: LayerDetails

class RulesResponse(BaseModel):
    count: int
    rules: List[Rule]
