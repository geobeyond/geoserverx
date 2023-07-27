from enum import Enum
from typing import List, Literal, Union, Optional

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


class ModeEnum(Enum):
    single = "SINGLE"
    opaque_container = "OPAQUE_CONTAINER"
    named = "NAMED"
    container = "CONTAINER"
    eo = "EO"


class WorkspaceModel(BaseModel):
    name: str = None


class BaseLayerGroup(BaseModel):
    name: str = ...


class SingleLayerGroup(BaseLayerGroup):
    mode: ModeEnum
    internationalTitle: str = ""
    internationalAbstract: str = ""
    publishables: PublishablesDict
    styles: StylesDict
    bounds: BoundsDict
    dateCreated: str = ...


class SingleLayerGroupModel(BaseModel):
    layerGroup: SingleLayerGroup


class LayerListModel(BaseModel):
    layer: List[str] = []


class LayerGroupModel(BaseModel):
    name: str
    mode: ModeEnum
    title: str
    layers: LayerListModel
    abstractTxt: Optional[str] = None
    workspace: Optional[WorkspaceModel] = None


class LayerGroupPayload(BaseModel):
    layerGroup: LayerGroupModel


class LayerGroupStylesModel(BaseModel):
    style: List[str] = []


class LayerGroupKeywordsModel(BaseModel):
    keyword: List[str] = []
