from dataclasses import dataclass
from typing import Union, Optional
from geoserverx.utils.logger import std_out_logger
from geoserverx.utils.enums import GSResponseEnum
from geoserverx.models.gs_response import GSResponse
from geoserverx.utils.errors import GeoServerXError
from geoserverx.models.style import StyleModel, AllStylesModel
import asyncio
from geoserverx.utils.http_client import AsyncClient
from geoserverx.utils.auth import GeoServerXAuth
from geoserverx.models.workspace import (
    NewWorkspace,
    NewWorkspaceInfo,
    WorkspaceModel,
    WorkspacesModel,
)
from geoserverx.models.data_store import (
    DataStoreModel,
    DataStoresModel,
    CreateDataStoreModel,
    CreateStoreItem,
    MainCreateDataStoreModel,
)
from geoserverx.models.layers import LayersModel, LayerModel
from geoserverx.models.coverages_store import CoveragesStoreModel, CoveragesStoresModel
from geoserverx.models.gs_response import GSResponse
from geoserverx.utils.services.async_datastore import (
    AddDataStoreProtocol,
    CreateFileStore,
    ShapefileStore,
    GPKGfileStore,
)
import json


@dataclass
class AsyncGeoServerX:
    """
    Async Geoserver client
    """

    username: str = "admin"
    password: str = "geoserver"
    url: str = "http://127.0.0.1:8080/geoserver/rest/"
    head = {"Content-Type": "application/json"}

    def __post_init__(self):
        if not self.username and not self.password and not self.url:
            raise GeoServerXError(0, "Username, Password and URL is missing")
        elif not self.username or self.username == "":
            raise GeoServerXError(0, "Username is missing")
        elif not self.password or self.password == "":
            raise GeoServerXError(0, "password is missing")
        elif not self.url or self.url == "":
            raise GeoServerXError(0, "URL is missing")
        self.http_client = AsyncClient(
            base_url=self.url,
            auth=(self.username, self.password),
        )

    async def __aenter__(self) -> "AsyncGeoServerX":
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self.http_client.aclose()

    @staticmethod
    def from_auth(
        auth: GeoServerXAuth,
    ) -> "AsyncGeoServerX":
        return AsyncGeoServerX(auth.username, auth.password, auth.url)

    def response_recognise(self, r) -> GSResponse:
        if r == 401:
            resp = GSResponseEnum._401.value
        elif r == 500:
            resp = GSResponseEnum._500.value
        elif r == 503:
            resp = GSResponseEnum._503.value
        elif r == 404:
            resp = GSResponseEnum._404.value
        elif r == 403:
            resp = GSResponseEnum._403.value
        elif r == 201:
            resp = GSResponseEnum._201.value
        elif r == 200:
            resp = GSResponseEnum._200.value
        elif r == 409:
            resp = GSResponseEnum._409.value
        return GSResponse.parse_obj(resp)

    # Get all workspaces
    async def get_all_workspaces(self) -> Union[WorkspacesModel, GSResponse]:
        Client = self.http_client
        responses = await Client.get(f"workspaces")
        if responses.status_code == 200:
            return WorkspacesModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    # Get specific workspaces
    async def get_workspace(self, workspace: str) -> Union[WorkspaceModel, GSResponse]:
        Client = self.http_client
        responses = await Client.get(f"workspaces/{workspace}")
        if responses.status_code == 200:
            return WorkspaceModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    # Create workspace
    async def create_workspace(
        self, name: str, default: bool = False, Isolated: bool = False
    ) -> GSResponse:
        Client = self.http_client
        payload: NewWorkspace = NewWorkspace(
            workspace=NewWorkspaceInfo(name=name, isolated=Isolated)
        )
        responses = await Client.post(
            f"workspaces?default={default}",
            data=payload.json(),
            headers=self.head,
        )
        results = self.response_recognise(responses.status_code)
        return results

    # Get vector stores in specific workspaces
    async def get_vector_stores_in_workspaces(self, workspace: str) -> DataStoresModel:
        Client = self.http_client
        responses = await Client.get(f"workspaces/{workspace}/datastores")
        if responses.status_code == 200:
            return DataStoresModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    # Get raster stores in specific workspaces
    async def get_raster_stores_in_workspaces(
        self, workspace: str
    ) -> CoveragesStoresModel:
        Client = self.http_client
        responses = await Client.get(f"workspaces/{workspace}/coveragestores")
        if responses.status_code == 200:
            return CoveragesStoresModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    # Get vector store information in specific workspaces
    async def get_vector_store(self, workspace: str, store: str) -> DataStoreModel:
        url = f"workspaces/{workspace}/datastores/{store}.json"
        Client = self.http_client
        responses = await Client.get(url)
        if responses.status_code == 200:
            return DataStoreModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    # Get raster  store information in specific workspaces
    async def get_raster_store(self, workspace: str, store: str) -> CoveragesStoreModel:
        url = f"workspaces/{workspace}/coveragestores/{store}.json"
        Client = self.http_client
        responses = await Client.get(url)
        if responses.status_code == 200:
            return CoveragesStoreModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    # Get all styles in GS
    async def get_allstyles(self) -> AllStylesModel:
        Client = self.http_client
        responses = await Client.get(f"styles")
        if responses.status_code == 200:
            return AllStylesModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    # Get specific style in GS
    async def get_style(self, style: str) -> StyleModel:
        Client = self.http_client
        responses = await Client.get(f"styles/{style}.json")
        if responses.status_code == 200:
            return StyleModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    # Add postgres db
    async def create_pg_store(
        self,
        name: str,
        workspace: str,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
    ) -> GSResponse:
        payload = MainCreateDataStoreModel(
            dataStore=CreateDataStoreModel(
                name=name,
                connectionParameters=CreateStoreItem(
                    host=host,
                    port=port,
                    database=database,
                    user=username,
                    passwd=password,
                    dbtype="postgis",
                ).dict(exclude_none=True),
            )
        )
        Client = self.http_client
        responses = await Client.post(
            f"workspaces/{workspace}/datastores/",
            data=payload.json(),
            headers=self.head,
        )
        results = self.response_recognise(responses.status_code)
        return results

    # Get all styles in GS
    async def get_allstyles(self) -> AllStylesModel:
        Client = self.http_client
        responses = await Client.get(f"styles")
        if responses.status_code == 200:
            return AllStylesModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    # Get specific style in GS
    async def get_style(self, style: str) -> StyleModel:
        Client = self.http_client
        responses = await Client.get(f"styles/{style}.json")
        if responses.status_code == 200:
            return StyleModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    async def create_file_store(self, workspace: str, store: str, file, service_type):
        service: AddDataStoreProtocol = CreateFileStore()

        if service_type == "shapefile":
            service = ShapefileStore(
                client=self.http_client,
                service=service,
                logger=std_out_logger("Shapefile"),
                file=file,
            )
        elif service_type == "gpkg":
            service = GPKGfileStore(
                client=self.http_client,
                service=service,
                logger=std_out_logger("GeoPackage"),
                file=file,
            )
        else:
            raise ValueError(f"Service type {service_type} not supported")
        responses = await service.addFile(self.http_client, workspace, store)
        return self.response_recognise(responses)

        if service_type == "shapefile":
            service = ShapefileStore(
                client=self.http_client,
                service=service,
                logger=std_out_logger("Shapefile"),
                file=file,
            )
        elif service_type == "gpkg":
            service = GPKGfileStore(
                service=service, logger=std_out_logger("GeoPackage"), file=file
            )
        else:
            raise ValueError(f"Service type {service_type} not supported")
        await service.addFile(self.http_client, workspace, store)

    # Get all layers
    async def get_all_layers(
        self, workspace: Optional[str] = None
    ) -> Union[LayersModel, GSResponse]:
        Client = self.http_client
        if workspace:
            responses = await Client.get(f"/workspaces/{workspace}/layers")
        else:
            responses = await Client.get(f"layers")
        if responses.status_code == 200:
            return LayersModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    # Get specific layer
    async def get_layer(
        self, workspace: str, layer: str
    ) -> Union[LayerModel, GSResponse]:
        Client = self.http_client
        responses = await Client.get(f"layers/{workspace}:{layer}")
        if responses.status_code == 200:
            return LayerModel.parse_obj(responses.json())
        else:
            results = self.response_recognise(responses.status_code)
            return results

    # Delete specific layer
    async def delete_layer(self, workspace: str, layer: str) -> GSResponse:
        Client = self.http_client
        responses = await Client.delete(f"layers/{workspace}:{layer}")
        results = self.response_recognise(responses.status_code)
        return results
