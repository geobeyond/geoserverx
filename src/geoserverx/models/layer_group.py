from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


class LayerGroupElement(BaseModel):
    name: str = ...
    href: str = ...


class LayerGroupList(BaseModel):
    layerGroup: List[LayerGroupElement] = ...


class LayerGroupsModel(BaseModel):
    layerGroups: Union[LayerGroupList, Literal[""]]


class PublishedDict(BaseModel):
    type: str = Field(..., alias="@type")
    name: str = ...
    href: str = ...


class PublishablesDict(BaseModel):
    published: PublishedDict = ...


class StyleDict(BaseModel):
    name: str = ...
    href: str = ...


class StylesDict(BaseModel):
    style: StyleDict = ...


class BoundsDict(BaseModel):
    minx: float = ...
    miny: float = ...
    maxx: float = ...
    maxy: float = ...
    crs: str = ...


class SingleLayerGroup(BaseModel):
    name: str = ...
    mode: Literal["SINGLE", "OPAQUE_CONTAINER", "NAMED", "CONTAINER", "EO"]
    internationalTitle: str = ""
    internationalAbstract: str = ""
    publishables: PublishablesDict
    styles: StylesDict
    bounds: BoundsDict
    dateCreated: str = ...


class SingleLayerGroupModel(BaseModel):
    layerGroup: SingleLayerGroup
