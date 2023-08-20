
from enum import Enum
from typing import Any, List, Optional, Dict, Union

from pydantic import BaseModel, Field


class Namespace(BaseModel):
    name: Optional[str] = Field(None, description='The name of the namespace.')
    href: Optional[str] = Field(None, description='URL to the namespace.')


class Keywords(BaseModel):
    string: Optional[List[str]] = Field(
        None,
        description='List of keyword values with internationalization and vocabulary',
    )


class MetadataLinkItem(BaseModel):
    type: Optional[str] = Field(None, description='The MIME type')
    metadataType: Optional[str] = Field(
        None, description='The type of metadata, e.g. "FGDC"'
    )
    content: Optional[str] = Field(None, description='The link URL')


class Metadatalinks(BaseModel):
    metadataLink: Optional[List[MetadataLinkItem]] = Field(
        None, description='A collection of metadata links for the resource.'
    )


class MetadataLinkItem1(BaseModel):
    type: Optional[str] = Field(None, description='The MIME type')
    content: Optional[str] = Field(None, description='The link URL')


class DataLinks(BaseModel):
    metadataLink: Optional[List[MetadataLinkItem1]] = Field(
        None, description='A collection of data links for the resource.'
    )
class CRSetnry(BaseModel):
    class Config:
        allow_population_by_field_name = True
    key: Optional[str] = Field(alias="@class")
    dollar: Optional[str] = Field(..., alias="$")


class CRSetnryDict(BaseModel):
    entry: CRSetnry

class NativeBoundingBox(BaseModel):
    minx: Optional[float] = Field(None, description='The min x coordinate')
    maxx: Optional[float] = Field(None, description='The max x coordinate')
    miny: Optional[float] = Field(None, description='The min y coordinate')
    maxy: Optional[float] = Field(None, description='The max y coordinate')
    crs: Optional[Union[str, CRSetnry]] = Field(
        None, description='The coordinate reference system object of the bounding box.'
    )


class LatLonBoundingBox(BaseModel):
    minx: Optional[float] = Field(None, description='The min x coordinate')
    maxx: Optional[float] = Field(None, description='The max x coordinate')
    miny: Optional[float] = Field(None, description='The min y coordinate')
    maxy: Optional[float] = Field(None, description='The max y coordinate')
    crs: Optional[str] = Field(
        None, description='The coordinate reference system object of the bounding box.'
    )


class Store(BaseModel):
    class Config:
        allow_population_by_field_name = True
    key: Optional[str] = Field(alias="@class")
    name: Optional[str] = Field(None, description='The name of the store')
    href: Optional[str] = Field(None, description='URL to the data store')


class ResponseSRS(BaseModel):
    string: Optional[str] = Field(None, description='The value of the srs')


class AttributeItem(BaseModel):
    name: Optional[str] = Field(None, description='Name of the attribute.')
    minOccurs: Optional[int] = Field(
        None, description='Minimum number of occurrences of the attribute.'
    )
    maxOccurs: Optional[int] = Field(
        None, description='Maximum number of occurrences of the attribute.'
    )
    nillable: Optional[bool] = Field(
        None,
        description='Flag indicating if null is an acceptable value for the attribute.',
    )
    binding: Optional[str] = Field(
        None, description='The java class that values of this attribute are bound to.'
    )
    length: Optional[int] 

class Attributes(BaseModel):
    attribute: Optional[List[AttributeItem]] = Field(
        None, description='The derived set of attributes for the feature type.'
    )


class _Key(Enum):
    regionateStrategy = 'regionateStrategy'
    regionateFeatureLimit = 'regionateFeatureLimit'
    cacheAgeMax = 'cacheAgeMax'
    cachingEnabled = 'cachingEnabled'
    regionateAttribute = 'regionateAttribute'
    indexingEnabled = 'indexingEnabled'
    dirName = 'dirName'




class MetadataEntryList(BaseModel):
    entry: Dict


class FeatureTypeInfo(BaseModel):
    name: Optional[str] = Field(
        None,
        description='The name of the resource. This name corresponds to the "published" name of the resource.',
    )
    nativeName: Optional[str] = Field(
        None,
        description='The native name of the resource. This name corresponds to the physical resource that feature type is derived from -- a shapefile name, a database table, etc...',
    )
    namespace: Optional[Namespace] = Field(
        None,
        description='The namespace URI of the resource. Example would be an application schema namespace URI.',
    )
    title: Optional[str] = Field(
        None,
        description='The title of the resource. This is usually something that is meant to be displayed in a user interface.',
    )
    abstract: Optional[str] = Field(
        None,
        description='A description of the resource. This is usually something that is meant to be displayed in a user interface.',
    )
    keywords: Optional[Keywords] = Field(
        None, description='A collection of keywords associated with the resource.'
    )
    srs: Optional[str] = Field(
        None,
        description='Returns the identifier of coordinate reference system of the resource.',
    )
    metadatalinks: Optional[Metadatalinks] 
    dataLinks: Optional[DataLinks] 
    
    nativeBoundingBox: Optional[NativeBoundingBox] = Field(
        None, description='Returns the bounds of the resource in its declared CRS.'
    )
    latLonBoundingBox: Optional[LatLonBoundingBox] = Field(
        None,
        description='The bounds of the resource in lat / lon. This value represents a "fixed value" and is not calculated on the underlying dataset.',
    )
    projectionPolicy:str
    metadata: Optional[MetadataEntryList] = Field(
        None, description='A list of key/value metadata pairs.'
    )
    store: Optional[Store] = Field(
        None, description='The store the resource is a part of.' 
    )
    nativeCRS:Optional[Union[str, CRSetnry]] = Field(
        None, description='String for Native CRS'
    )
    cqlFilter: Optional[str] = Field(
        None, description='The ECQL string used as default feature type filter'
    )
    maxFeatures: Optional[int] = Field(
        None,
        description='A cap on the number of features that a query against this type can return.',
    )
    numDecimals: Optional[int] = Field(
        None,
        description='The number of decimal places to use when encoding floating point numbers from data of this feature type.',
    )
    responseSRS: Optional[ResponseSRS] = Field(
        None,
        description='The SRSs that the WFS service will advertise in the capabilities document for this feature type (overriding the global WFS settings).',
    )
    overridingServiceSRS: Optional[bool] = Field(
        None,
        description='True if this feature type info is overriding the WFS global SRS list',
    )
    skipNumberMatched: Optional[bool] = Field(
        None,
        description='True if this feature type info is overriding the counting of numberMatched.',
    )
    circularArcPresent: Optional[bool] = None
    linearizationTolerance: Optional[float] = Field(
        None,
        description='Tolerance used to linearize this feature type, as an absolute value expressed in the geometries own CRS',
    )
    attributes: Optional[Attributes] = Field(
        None,
        description='Wrapper for the derived set of attributes for the feature type.',
    )
    enabled:Optional[bool]
    advertised:Optional[bool]
    serviceConfiguration:Optional[bool]
    simpleConversionEnabled:Optional[bool]
    padWithZeros:Optional[bool]
    forcedDecimal:Optional[bool]
    overridingServiceSRS:Optional[bool]
    skipNumberMatched:Optional[bool]
    circularArcPresent:Optional[bool]
    encodeMeasures:Optional[bool]

class FeatureTypesModel(BaseModel):
    featureType : FeatureTypeInfo 