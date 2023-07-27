from typing import List, Optional, Union
from pydantic import BaseModel, Field


class LayerInBulk(BaseModel):
    name: str = ...
    href: str = ...


class LayerDict(BaseModel):
    layer: List[LayerInBulk]


class LayersModel(BaseModel):
    layers: Union[LayerDict, str] = ""


class DefaultStyleOfLayer(BaseModel):
    name: str = ...
    href: str = ...


class ExtraStyles(BaseModel):
    _class: str = Field(..., alias="@class")
    style: List[DefaultStyleOfLayer]


class LayerResource(BaseModel):
    _class: str = Field(..., alias="@class")
    name: str = ...
    href: str = ...


class LayerAttribution(BaseModel):
    logoWidth: float = ...
    logoHeight: float = ...


class SingleLayer(BaseModel):
    name: str = ...
    path: str = ...
    type: str = ...
    defaultStyle: DefaultStyleOfLayer = ...
    styles: Optional[ExtraStyles] = None
    resource: LayerResource = ...
    attribution: LayerAttribution
    dateCreated: Optional[str] = None


class LayerModel(BaseModel):
    layer: SingleLayer = ...


# class NewWorkspaceInfo(BaseModel):
#     name: str = ...
#     isolated: bool = None


# class NewWorkspace(BaseModel):
#     workspace: NewWorkspaceInfo = ...
