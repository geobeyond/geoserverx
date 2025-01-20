import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Union

import httpx

from ..models.coverages_layer import CoverageModel
from ..models.coverages_store import CoveragesStoreModelDetail, CoveragesStoresModel
from ..models.data_store import (
    CreateDataStoreModel,
    CreateStoreItem,
    DataStoreModelDetails,
    DataStoresModel,
    MainCreateDataStoreModel,
)
from ..models.geofence import Rule, RulesResponse
from ..models.gs_response import GSResponse
from ..models.layer_group import LayerGroupsModel
from ..models.layers import LayersModel, SingleLayer
from ..models.style import AllStyleList, SingleStyle
from ..models.workspace import UpdateWorkspaceInfo, WorkspaceModel, workspaceDict
from ..utils.auth import GeoServerXAuth
from ..utils.custom_exceptions import GSModuleNotFound
from ..utils.enums import GSResponseEnum
from ..utils.errors import GeoServerXError
from ..utils.http_client import AsyncClient
from ..utils.logger import std_out_logger
from ..utils.services.async_datastore import (
    AddDataStoreProtocol,
    CreateFileStore,
    GpkgFileStore,
    ShapefileStore,
)


class StoreType(Enum):
    """Enum for GeoServer store types"""

    raster = "raster"
    vector = "vector"


@dataclass
class AsyncGeoServerX:
    """
    Class to interact with GeoServer for async operations such as uploading,
    deleting, and checking resources.
    Initialize the GeoServer async utility.

    Args:
        base_url (str): Base URL of the GeoServer instance.
        username (str): GeoServer username.
        password (str): GeoServer password.
    """

    username: str = "admin"
    password: str = "geoserver"
    url: str = "http://127.0.0.1:8080/geoserver/rest/"
    headers: Dict[str, str] = field(
        default_factory=lambda: {
            "Content-Type": "application/json",
        }
    )

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

    def recognize_response(self, response) -> GSResponse:
        if response == 401:
            resp = GSResponseEnum._401.value
        elif response == 500:
            resp = GSResponseEnum._500.value
        elif response == 503:
            resp = GSResponseEnum._503.value
        elif response == 404:
            resp = GSResponseEnum._404.value
        elif response == 403:
            resp = GSResponseEnum._403.value
        elif response == 201:
            resp = GSResponseEnum._201.value
        elif response == 409:
            resp = GSResponseEnum._409.value
        elif response == 200:
            resp = GSResponseEnum._200.value
        return GSResponse.model_validate(resp)

    # check if certain module/plugin exists in geoserver
    async def check_modules(self, name) -> Union[bool, GSResponse]:
        """
        Check if a specific module or plugin is available in GeoServer.

        Args:
            name (str): Name of the module to check.

        Returns:
            Union[bool, GSResponse]: True if the module exists, otherwise a GSResponse object.
        """
        client = self.http_client
        try:
            response = await client.get("about/status.json")
            response.raise_for_status()  # Raises an HTTPError for bad response (4xx and 5xx)

            # Extract and check the modules
            installed_modules = [
                item["name"].lower() for item in response.json()["statuss"]["status"]
            ]
            if name.lower() in installed_modules:
                return True
            raise GSModuleNotFound(f"'{name}' plugin not found")

        except httpx.HTTPStatusError as e:
            # Handle HTTP errors (e.g., 4xx, 5xx)
            return self.recognize_response(e.response.status_code)
        except httpx.RequestError as e:
            # Handle other request errors (e.g., network problems)
            return self.recognize_response(e.response.status_code)
        except GSModuleNotFound as e:
            # Handle Module not found exception
            return GSResponse(code=412, response=str(e))

    async def get_all_workspaces(self) -> Union[workspaceDict, GSResponse]:
        """
        Retrieve a list of all workspaces from GeoServer.

        Returns:
            Union[workspaceDict, GSResponse]: A list of WorkspaceInBulk objects if successful,
            or a GSResponse object containing error details if the request fails.
        """
        client = self.http_client
        complete_response = await client.get("workspaces")
        if complete_response.status_code == 200:
            response_json = complete_response.json()
            workspaces_data = response_json.get("workspaces", response_json)
            return workspaceDict(**workspaces_data)

        return self.recognize_response(complete_response.status_code)

    async def get_workspace(self, workspace: str) -> Union[WorkspaceModel, GSResponse]:
        """
        Retrieve information about a specific GeoServer workspace.

        Args:
            workspace (str): The name of the workspace to retrieve.

        Returns:
            Union[WorkspaceModel, GSResponse]: Returns either:
                - WorkspaceModel: If the workspace exists (status code 200)
                - GSResponse: If there's an error or workspace doesn't exist
        """
        client = self.http_client
        response = await client.get(f"workspaces/{workspace}")
        if response.status_code == 200:
            return WorkspaceModel.model_validate(response.json())
        return self.recognize_response(response.status_code)

    async def delete_workspace(
        self, workspace: str, recurse: bool = False
    ) -> GSResponse:
        """
        Delete a GeoServer workspace.

        Args:
            workspace (str): The name of the workspace to delete
            recurse (bool, optional): If True, recursively deletes all resources
                contained within the workspace. Defaults to False.
        Returns:
            GSResponse: Response object indicating success or failure.
        """
        client = self.http_client
        response = await client.delete(
            f"workspaces/{workspace}", params={"recurse": recurse}
        )
        return self.recognize_response(response.status_code)

    async def create_workspace(
        self, name: str, default: bool = False, isolated: bool = False
    ) -> GSResponse:
        """
        Create a new workspace in GeoServer.

        Args:
            name (str): Name of the workspace to create
            default (bool, optional): Set this workspace as the default workspace. Defaults to False.
            isolated (bool, optional): Enable workspace isolation. When True, the workspace
                will have its own service URLs. Defaults to False.
        Returns:
            GSResponse: Response object indicating success or failure.
        """
        client = self.http_client
        new_ws = json.dumps({"workspace": {"name": name, "isolated": isolated}})
        response = await client.post(
            "workspaces",
            data=new_ws,
            headers=self.headers,
            params={"default": default},
        )
        return self.recognize_response(response.status_code)

    async def update_workspace(
        self, name: str, update: UpdateWorkspaceInfo
    ) -> GSResponse:
        """
        Update an existing workspace in GeoServer.

        Args:
            name (str): Name of the workspace to update
            update (UpdateWorkspaceInfo): Object containing the workspace properties to update

        Returns:
            GSResponse: Response object indicating success or failure:
        """
        client = self.http_client
        update_ws = json.dumps({"workspace": update.model_dump(exclude_none=True)})
        response = await client.put(
            f"workspaces/{name}.json",
            data=update_ws,
            headers=self.headers,
        )
        return self.recognize_response(response.status_code)

    async def get_vector_stores_in_workspaces(self, workspace: str) -> DataStoresModel:
        """
        Retrieve all vector data stores within a specified workspace.

        Args:
            workspace (str): Name of the workspace to query for data stores

        Returns:
            DataStoresModel: A model containing a list of data stores if successful
        """
        client = self.http_client
        response = await client.get(f"workspaces/{workspace}/datastores")
        if response.status_code == 200:
            return DataStoresModel(**response.json())
        return self.recognize_response(response.status_code)

    async def get_raster_stores_in_workspaces(
        self, workspace: str
    ) -> CoveragesStoresModel:
        """
        Retrieve all raster (coverage) stores within a specified workspace.

        Args:
            workspace (str): Name of the workspace to query for coverage stores

        Returns:
            CoveragesStoresModel: A model containing a list of coverage stores if successful
            GSResponse: Error response if the request fails
        """
        client = self.http_client
        response = await client.get(f"workspaces/{workspace}/coveragestores")
        if response.status_code == 200:
            return CoveragesStoresModel(**response.json())
        return self.recognize_response(response.status_code)

    async def get_vector_store(
        self, workspace: str, store: str
    ) -> DataStoreModelDetails:
        """
        Retrieve details of a specific vector data store from a workspace.

        Args:
            workspace (str): Name of the workspace containing the store
            store (str): Name of the vector data store to retrieve

        Returns:
            DataStoreModelDetails: Details of the requested vector store if successful
            GSResponse: Error response if the request fails
        """
        url = f"workspaces/{workspace}/datastores/{store}.json"
        client = self.http_client
        response = await client.get(url)
        if response.status_code == 200:
            response_json = response.json()
            datastord_data = response_json.get("dataStore", response_json)
            return DataStoreModelDetails(**datastord_data)
        return self.recognize_response(response.status_code)

    async def get_raster_store(
        self, workspace: str, store: str
    ) -> CoveragesStoreModelDetail:
        """
        Retrieve details of a specific raster (coverage) store from a workspace.

        Args:
            workspace (str): Name of the workspace containing the store
            store (str): Name of the raster store to retrieve

        Returns:
            CoveragesStoreModelDetail: Details of the requested raster store if successful
            GSResponse: Error response if the request fails
        """
        url = f"workspaces/{workspace}/coveragestores/{store}.json"
        client = self.http_client
        response = await client.get(url)
        if response.status_code == 200:
            response_json = response.json()
            datastord_data = response_json.get("coverageStore", response_json)
            return CoveragesStoreModelDetail(**datastord_data)
        return self.recognize_response(response.status_code)

    async def delete_store(
        self, workspace: str, store: str, type: StoreType, recurse: bool = False
    ) -> GSResponse:
        """
        Create a new data store (vector) or coverage store (raster) in a specified workspace.

        Args:
            workspace (str): Name of the workspace where the store will be created
            store (Union[CoverageStoreModel, DataStoreModelDetails]): Store configuration model
                - CoverageStoreModel: For raster data stores
                - DataStoreModelDetails: For vector data stores
            type (StoreType): Type of store to create, either "raster" or "vector"
                - "raster": Creates a coverage store for raster data
                - "vector": Creates a data store for vector data
            recurse (bool, optional): If True, recursively deletes all resources
                contained within the store. Defaults to False.

        Returns:
            GSResponse: Response object indicating success or failure
        """

        client = self.http_client
        if type == "raster":
            response = await client.delete(
                f"/workspaces/{workspace}/coveragestores/{store}",
                params={"recurse": recurse},
                headers=self.headers,
            )
        elif type == "vector":
            response = await client.delete(
                f"/workspaces/{workspace}/datastores/{store}",
                params={"recurse": recurse},
                headers=self.headers,
            )
        return self.recognize_response(response.status_code)

    async def get_all_styles(self) -> AllStyleList:
        """
        Retrieve all styles configured in GeoServer.

        Returns:
            AllStyleList: List of all available styles and their configurations
            GSResponse: Response object indicating failure
        """
        client = self.http_client
        complete_response = await client.get("styles")
        if complete_response.status_code == 200:
            response_json = complete_response.json()
            style_data = response_json.get("styles", response_json)
            return AllStyleList(**style_data)
        return self.recognize_response(complete_response.status_code)

    async def get_style(self, style: str) -> SingleStyle:
        """
        Retrieve a specific style configuration from GeoServer.

        Args:
            style (str): Name of the style to retrieve

        Returns:
            SingleStyle: Configuration details of the requested style
            GSResponse: Response object indicating failure
        """
        client = self.http_client
        complete_response = await client.get(f"styles/{style}.json")
        if complete_response.status_code == 200:
            response_json = complete_response.json()
            style_data = response_json.get("style", response_json)
            return SingleStyle(**style_data)

        return self.recognize_response(complete_response.status_code)

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
        """
        Create a new PostgreSQL/PostGIS data store in GeoServer.

        Args:
            name (str): Name of the store to create
            workspace (str): Name of the workspace where the store will be created
            host (str): PostgreSQL server hostname
            port (int): PostgreSQL server port
            username (str): Database username
            password (str): Database password
            database (str): Name of the database

        Returns:
            GSResponse: Response object indicating success or failure
        """
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
                ).model_dump(exclude_none=True),
            )
        )
        client = self.http_client
        response = await client.post(
            f"workspaces/{workspace}/datastores/",
            data=payload.model_dump_json(),
            headers=self.headers,
        )
        return self.recognize_response(response.status_code)

    async def create_file_store(self, workspace: str, store: str, file, service_type):
        """
        Create a new file-based data store in GeoServer.

        Args:
            workspace (str): Name of the workspace where the store will be created
            store (str): Name of the store to create
            file: File object to be uploaded
            service_type (str): Type of file store to create ('shapefile' or 'gpkg')

        Returns:
            GSResponse: Response object indicating success or failure
        """
        service: AddDataStoreProtocol = CreateFileStore()

        if service_type == "shapefile":
            service = ShapefileStore(
                client=self.http_client,
                service=service,
                logger=std_out_logger("Shapefile"),
                file=file,
            )
        elif service_type == "gpkg":
            service = GpkgFileStore(
                client=self.http_client,
                service=service,
                logger=std_out_logger("GeoPackage"),
                file=file,
            )
        else:
            raise ValueError(f"Service type {service_type} not supported")
        response = await service.add_file(self.http_client, workspace, store)
        return self.recognize_response(response)

    async def get_all_layers(
        self, workspace: Optional[str] = None
    ) -> Union[LayersModel, GSResponse]:
        """
        Retrieve all layers configured in GeoServer.

        Args:
            workspace (Optional[str]): Name of the workspace to filter layers.
                                     If None, returns layers from all workspaces.

        Returns:
            LayersModel: List of all available layers and their configurations
            GSResponse: Response object indicating failure
        """
        client = self.http_client
        if workspace:
            response = await client.get(f"/workspaces/{workspace}/layers")
        else:
            response = await client.get("layers")
        if response.status_code == 200:
            return LayersModel(**response.json())
        return self.recognize_response(response.status_code)

    async def get_layer(
        self, workspace: str, layer: str, detail: bool = False
    ) -> Union[SingleLayer, CoverageModel, GSResponse]:
        """
        Retrieve layer information from GeoServer, with optional detailed information.

        Args:
            workspace (str): Name of the workspace containing the layer
            layer (str): Name of the layer to retrieve
            detail (bool, optional): If True, returns detailed layer information including
                specific vector or raster properties. Defaults to False.

        Returns:
            Union[SingleLayer, GSResponse]: One of the following:
                - LayerModel: Basic layer information if detail=False
                - CoverageModel: Detailed raster layer information if detail=True and layer is raster
                - GSResponse: Error response if the request fails
        """
        client = self.http_client
        response = await client.get(f"layers/{workspace}:{layer}")
        if response.status_code == 200:
            response_json = response.json()
            if detail:

                if response_json["layer"]["type"] == "VECTOR":
                    result = self.get_vector_layer(
                        workspace,
                        response_json["layer"]["resource"]["href"].split("/")[-3],
                        layer,
                    )
                    return result
                elif response_json["layer"]["type"] == "RASTER":
                    result = self.get_raster_layer(
                        workspace,
                        response_json["layer"]["resource"]["name"].split(":")[1],
                        layer,
                    )
                    return result
            else:

                layer_data = response_json.get("layer", response_json)
                return SingleLayer(**layer_data)
        else:
            return self.recognize_response(response.status_code)

    async def delete_layer(self, workspace: str, layer: str) -> GSResponse:
        """
        Delete a layer from a specified workspace in GeoServer.

        Args:
            workspace (str): Name of the workspace containing the layer
            layer (str): Name of the layer to delete

        Returns:
            GSResponse: Response object indicating success or failure
        """
        client = self.http_client
        response = await client.delete(f"layers/{workspace}:{layer}")
        return self.recognize_response(response.status_code)

    async def get_all_layer_groups(
        self, workspace: Optional[str] = None
    ) -> Union[LayerGroupsModel, GSResponse]:
        """
        Retrieve all layer groups from GeoServer, optionally filtered by workspace.

        Args:
            workspace (Optional[str]): Name of the workspace to filter layer groups.
                If None, retrieves layer groups from all workspaces.

        Returns:
            Union[LayerGroupsModel, GSResponse]: Either a list of layer groups or an error response
                - LayerGroupsModel: Contains a list of all layer groups if successful
                - GSResponse: Error response if the request fails
        """
        client = self.http_client
        if workspace:
            response = await client.get(f"workspaces/{workspace}/layergroups")
        else:
            response = await client.get("layergroups")
        if response.status_code == 200:
            return LayerGroupsModel(**response.json())
        return self.recognize_response(response.status_code)

    async def get_all_geofence_rules(self) -> Union[RulesResponse, GSResponse]:
        """
        Retrieve all GeoFence rules configured in GeoServer.

        Returns:
            Union[RulesResponse, GSResponse]: Either a list of all rules or an error response
                - RulesResponse: Contains a list of all GeoFence rules if successful
                - GSResponse: Error response if the request fails
        """
        client = self.http_client
        # Check if the geofence plugin exists
        module_check = await self.check_modules("geofence")
        # If the module check fails, return the GSResponse directly
        if isinstance(module_check, GSResponse):
            return module_check
        response = await client.get(
            "geofence/rules/", headers={"Accept": "application/json"}
        )
        if response.status_code == 200:
            return RulesResponse(**response.json())
        return self.recognize_response(response.status_code)

    async def get_geofence_rule(self, id: int) -> Union[Rule, GSResponse]:
        """
        Retrieve a specific GeoFence rule by its ID from GeoServer.

        Args:
            id (int): The unique identifier of the GeoFence rule to retrieve

        Returns:
            Union[Rule, GSResponse]: Either the requested rule or an error response
                - Rule: The rule details if found
                - GSResponse: Error response if the request fails
        """
        client = self.http_client
        # Check if the geofence plugin exists
        module_check = await self.check_modules("geofence")
        # If the module check fails, return the GSResponse directly
        if isinstance(module_check, GSResponse):
            return module_check
        response = await client.get(f"geofence/rules/id/{id}", headers=self.headers)
        if response.status_code == 200:
            return Rule(**response.json())
        return self.recognize_response(response.status_code)

    async def create_geofence(self, rule: Rule) -> GSResponse:
        """
        Create a new GeoFence rule in GeoServer.

        Args:
            rule (Rule): Rule object containing the GeoFence rule configuration details.
                The Rule object should specify access control parameters such as:
                - workspace
                - layer
                - access rights
                - user/role information
                - service type
                - request type

        Returns:
            GSResponse: Response object indicating success or failure
        """
        PostingRule = json.dumps({"Rule": rule.model_dump(exclude_none=True)})
        # Check if the geofence plugin exists
        module_check = await self.check_modules("geofence")
        # If the module check fails, return the GSResponse directly
        if isinstance(module_check, GSResponse):
            return module_check
        client = self.http_client
        response = await client.post(
            "geofence/rules",
            content=PostingRule,
            headers=self.headers,
        )
        return self.recognize_response(response.status_code)
