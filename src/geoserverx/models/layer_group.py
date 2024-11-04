from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


class LayerGroupElement(BaseModel):
    name: str = ...
    href: str = ...


class LayerGroupList(BaseModel):
    layerGroup: List[LayerGroupElement] = ...


class LayerGroupsModel(BaseModel):
    layerGroups: Union[LayerGroupList, Literal[""]]


class Published(BaseModel):
    type: str = Field(..., alias="@type")
    name: str = ...
    href: str = ...


class Publishables(BaseModel):
    published: Published = ...


class Style(BaseModel):
    name: str = ...
    href: str = ...


class Styles(BaseModel):
    style: Style = ...


class Bounds(BaseModel):
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
    publishables: Publishables
    styles: Styles
    bounds: Bounds
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
