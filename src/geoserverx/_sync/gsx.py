from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Union

import httpx
from pydantic import ValidationError

from ..models.coverages_layer import CoverageModel
from ..models.coverages_store import CoveragesStoreModel, CoveragesStoresModel
from ..models.data_store import (
    CreateDataStoreModel,
    CreateStoreItem,
    DataStoreModel,
    DataStoresModel,
    MainCreateDataStoreModel,
)
from ..models.featuretypes_layer import FeatureTypesModel
from ..models.geofence import GetRule, NewRule, Rule, RulesResponse
from ..models.gs_response import GSResponse
from ..models.layer_group import LayerGroupsModel
from ..models.layers import LayerModel, LayersModel
from ..models.style import AllStylesModel, StyleModel
from ..models.workspace import (
    NewWorkspace,
    NewWorkspaceInfo,
    UpdateWorkspace,
    UpdateWorkspaceInfo,
    WorkspaceModel,
    WorkspacesModel,
)
from ..utils.auth import GeoServerXAuth
from ..utils.custom_exceptions import GSModuleNotFound
from ..utils.enums import GSResponseEnum
from ..utils.errors import GeoServerXError
from ..utils.http_client import SyncClient
from ..utils.logger import std_out_logger
from ..utils.services.datastore import (
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
class SyncGeoServerX:
    """
    Class to interact with GeoServer for syncing operations such as uploading,
    deleting, and checking resources.
    Initialize the GeoServer sync utility.

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
        self.http_client = SyncClient(
            base_url=self.url,
            auth=(self.username, self.password),
        )

    def __enter__(self) -> "SyncGeoServerX":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self.http_client.aclose()

    @staticmethod
    def from_auth(
        auth: GeoServerXAuth,
    ) -> "SyncGeoServerX":
        return SyncGeoServerX(auth.username, auth.password, auth.url)

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

    def exception_handler(func):
        def inner_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except httpx.ConnectError:
                return GSResponse(code=503, response="Error in connecting to Geoserver")
            except httpx.TimeoutException:
                return GSResponse(code=504, response="Timeout Error in connection")

        return inner_function

    # check if certain module/plugin exists in geoserver
    @exception_handler
    def check_modules(self, name) -> Union[bool, GSResponse]:
        """
        Check if a specific module or plugin is available in GeoServer.

        Args:
            name (str): Name of the module to check.

        Returns:
            Union[bool, GSResponse]: True if the module exists, otherwise a GSResponse object.
        """
        client = self.http_client
        try:
            response = client.get("about/status.json")
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

    @exception_handler
    def get_all_workspaces(self) -> Union[WorkspacesModel, GSResponse]:
        """
        Retrieve a list of all workspaces from GeoServer.

        Returns:
            Union[WorkspacesModel, GSResponse]: A WorkspacesModel containing the list of workspaces if successful,
            or a GSResponse object containing error details if the request fails.
        """
        client = self.http_client
        response = client.get("workspaces")
        if response.status_code == 200:
            return WorkspacesModel.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_workspace(self, workspace: str) -> Union[WorkspaceModel, GSResponse]:
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
        response = client.get(f"workspaces/{workspace}")
        if response.status_code == 200:
            return WorkspaceModel.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def delete_workspace(self, workspace: str, recurse: bool = False) -> GSResponse:
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
        response = client.delete(f"workspaces/{workspace}", params={"recurse": recurse})
        return self.recognize_response(response.status_code)

    @exception_handler
    def create_workspace(
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
        payload: NewWorkspace = NewWorkspace(
            workspace=NewWorkspaceInfo(name=name, isolated=isolated)
        )
        client = self.http_client
        response = client.post(
            "workspaces",
            content=payload.model_dump_json(),
            params={"default": default},
            headers=self.headers,
        )
        return self.recognize_response(response.status_code)

    @exception_handler
    def update_workspace(self, name: str, update: UpdateWorkspaceInfo) -> GSResponse:
        """
        Update an existing workspace in GeoServer.

        Args:
            name (str): Name of the workspace to update
            update (UpdateWorkspaceInfo): Object containing the workspace properties to update

        Returns:
            GSResponse: Response object indicating success or failure:
        """
        client = self.http_client
        update_ws = UpdateWorkspace(workspace=update)
        response = client.put(
            f"workspaces/{name}.json",
            data=update_ws.model_dump_json(exclude_none=True),
            headers=self.headers,
        )
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_vector_stores_in_workspaces(self, workspace: str) -> DataStoresModel:
        """
        Retrieve all vector data stores within a specified workspace.

        Args:
            workspace (str): Name of the workspace to query for data stores

        Returns:
            DataStoresModel: A model containing a list of data stores if successful
        """
        client = self.http_client
        response = client.get(f"workspaces/{workspace}/datastores")
        if response.status_code == 200:
            return DataStoresModel.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_raster_stores_in_workspaces(self, workspace: str) -> CoveragesStoresModel:
        """
        Retrieve all raster (coverage) stores within a specified workspace.

        Args:
            workspace (str): Name of the workspace to query for coverage stores

        Returns:
            CoveragesStoresModel: A model containing a list of coverage stores if successful
            GSResponse: Error response if the request fails
        """
        client = self.http_client
        response = client.get(f"workspaces/{workspace}/coveragestores")
        if response.status_code == 200:
            return CoveragesStoresModel.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_vector_store(self, workspace: str, store: str) -> DataStoreModel:
        """
        Retrieve details of a specific vector data store from a workspace.

        Args:
            workspace (str): Name of the workspace containing the store
            store (str): Name of the vector data store to retrieve

        Returns:
            DataStoreModel: Details of the requested vector store if successful
            GSResponse: Error response if the request fails
        """
        url = f"workspaces/{workspace}/datastores/{store}.json"
        client = self.http_client
        response = client.get(url)
        if response.status_code == 200:
            return DataStoreModel.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def create_vector_store(self, workspace: str, store: DataStoresModel) -> GSResponse:
        """
        Create a new vector data store in a specified workspace.

        Args:
            workspace (str): Name of the workspace where the store will be created
            store (DataStoresModel): Model containing the vector store configuration details

        Returns:
            GSResponse: Response object indicating success or failure
        """

        client = self.http_client
        response = client.post(
            f"workspaces/{workspace}/datastores",
            content=store.model_dump_json(),
            headers=self.headers,
        )
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_raster_store(self, workspace: str, store: str) -> CoveragesStoreModel:
        """
        Retrieve details of a specific raster (coverage) store from a workspace.

        Args:
            workspace (str): Name of the workspace containing the store
            store (str): Name of the raster store to retrieve

        Returns:
            CoveragesStoreModel: Details of the requested raster store if successful
            GSResponse: Error response if the request fails
        """

        url = f"workspaces/{workspace}/coveragestores/{store}.json"
        client = self.http_client
        response = client.get(url)
        if response.status_code == 200:
            return CoveragesStoreModel.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def create_raster_store(
        self, workspace: str, store: CoveragesStoreModel
    ) -> GSResponse:
        """
        Create a new raster (coverage) store in a specified workspace.

        Args:
            workspace (str): Name of the workspace where the store will be created
            store (CoveragesStoreModel): Model containing the raster store configuration details

        Returns:
            GSResponse: Response object indicating success or failure
        """

        client = self.http_client
        response = client.post(
            f"workspaces/{workspace}/coveragestores",
            content=store.model_dump_json(),
            headers=self.headers,
        )
        return self.recognize_response(response.status_code)

    @exception_handler
    def delete_store(self, workspace: str, store: str, type: StoreType) -> GSResponse:
        """
        Create a new data store (vector) or coverage store (raster) in a specified workspace.

        Args:
            workspace (str): Name of the workspace where the store will be created
            store (Union[CoverageStoreModel, DataStoreModel]): Store configuration model
                - CoverageStoreModel: For raster data stores
                - DataStoreModel: For vector data stores
            type (StoreType): Type of store to create, either "raster" or "vector"
                - "raster": Creates a coverage store for raster data
                - "vector": Creates a data store for vector data

        Returns:
            GSResponse: Response object indicating success or failure
        """

        client = self.http_client
        if type == "raster":
            response = client.delete(
                f"/workspaces/{workspace}/coveragestores/{store}", headers=self.headers
            )
        elif type == "vector":
            response = client.delete(
                f"/workspaces/{workspace}/datastores/{store}", headers=self.headers
            )
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_all_styles(self) -> AllStylesModel:
        """
        Retrieve all styles configured in GeoServer.

        Returns:
            AllStylesModel: List of all available styles and their configurations
            GSResponse: Response object indicating failure
        """

        client = self.http_client
        response = client.get("styles")
        if response.status_code == 200:
            return AllStylesModel.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_style(self, style: str) -> StyleModel:
        """
        Retrieve a specific style configuration from GeoServer.

        Args:
            style (str): Name of the style to retrieve

        Returns:
            StyleModel: Configuration details of the requested style
            GSResponse: Response object indicating failure
        """

        client = self.http_client
        response = client.get(f"styles/{style}.json")
        if response.status_code == 200:
            return StyleModel.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def create_file_store(
        self, workspace: str, store: str, file, service_type
    ) -> GSResponse:
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
                service=service, logger=std_out_logger("Shapefile"), file=file
            )
        elif service_type == "gpkg":
            service = GpkgFileStore(
                service=service, logger=std_out_logger("GeoPackage"), file=file
            )
        else:
            raise ValueError(f"Service type {service_type} not supported")
        response = service.add_file(self.http_client, workspace, store)
        return self.recognize_response(response)

    @exception_handler
    def create_pg_store(
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
        response = client.post(
            f"workspaces/{workspace}/datastores/",
            data=payload.model_dump_json(),
            headers=self.headers,
        )
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_all_layers(
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
            response = client.get(f"/workspaces/{workspace}/layers")
        else:
            response = client.get("layers")
        if response.status_code == 200:
            return LayersModel.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_vector_layer(
        self, workspace: str, store: str, layer: str
    ) -> Union[FeatureTypesModel, GSResponse]:
        """
        Retrieve configuration details of a vector layer from GeoServer.

        Args:
            workspace (str): Name of the workspace containing the layer
            store (str): Name of the data store containing the layer
            layer (str): Name of the vector layer to retrieve

        Returns:
            FeatureTypesModel: Configuration details of the vector layer
            GSResponse: Response object indicating failure
        """

        client = self.http_client
        response = client.get(
            f"/workspaces/{workspace}/datastores/{store}/featuretypes/{layer}.json"
        )
        if response.status_code == 200:
            try:
                return FeatureTypesModel.parse_obj(response.json())
            except ValidationError as validation_error:
                print("Pydantic Validation Error:")
                print(validation_error)
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_raster_layer(
        self, workspace: str, store: str, layer: str
    ) -> Union[CoverageModel, GSResponse]:
        """
        Retrieve configuration details of a raster layer from GeoServer.

        Args:
            workspace (str): Name of the workspace containing the layer
            store (str): Name of the coverage store containing the layer
            layer (str): Name of the raster layer to retrieve

        Returns:
            CoverageModel: Configuration details of the raster layer
            GSResponse: Response object indicating failure
        """

        client = self.http_client
        response = client.get(
            f"/workspaces/{workspace}/coveragestores/{store}/coverages/{layer}.json"
        )
        if response.status_code == 200:
            return CoverageModel.parse_obj(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_layer(
        self, workspace: str, layer: str, detail: bool = False
    ) -> Union[LayerModel, FeatureTypesModel, GSResponse]:
        """
        Retrieve layer information from GeoServer, with optional detailed information.

        Args:
            workspace (str): Name of the workspace containing the layer
            layer (str): Name of the layer to retrieve
            detail (bool, optional): If True, returns detailed layer information including
                specific vector or raster properties. Defaults to False.

        Returns:
            Union[LayerModel, FeatureTypesModel, GSResponse]: One of the following:
                - LayerModel: Basic layer information if detail=False
                - FeatureTypesModel: Detailed vector layer information if detail=True and layer is vector
                - CoverageModel: Detailed raster layer information if detail=True and layer is raster
                - GSResponse: Error response if the request fails
        """

        client = self.http_client
        response = client.get(f"layers/{workspace}:{layer}")
        if response.status_code == 200:
            if detail:
                res = response.json()
                if res["layer"]["type"] == "VECTOR":
                    result = self.get_vector_layer(
                        workspace,
                        res["layer"]["resource"]["href"].split("/")[-3],
                        layer,
                    )
                    return FeatureTypesModel.parse_obj(result.dict())
                elif res["layer"]["type"] == "RASTER":
                    result = self.get_raster_layer(
                        workspace, res["layer"]["resource"]["name"].split(":")[1], layer
                    )
                    return CoverageModel.parse_obj(result.dict())
            else:
                return LayerModel.parse_obj(response.json())
        else:
            return self.recognize_response(response.status_code)

    @exception_handler
    def create_vector_layer(
        self, workspace: str, layer: FeatureTypesModel
    ) -> GSResponse:
        """
        Create a new vector layer (feature type) in a specified workspace.

        Args:
            workspace (str): Name of the workspace where the layer will be created
            layer (FeatureTypesModel): Model containing the vector layer configuration details,
                including metadata, attribute information, and other feature type parameters

        Returns:
            GSResponse: Response object indicating success or failure
        """
        client = self.http_client
        response = client.post(
            f"/workspaces/{workspace}/featuretypes",
            data=layer.model_dump(by_alias=True, exclude_none=True),
            headers=self.headers,
        )
        return self.recognize_response(response.status_code)

    @exception_handler
    def create_raster_layer(self, workspace: str, layer: CoverageModel) -> GSResponse:
        """
        Create a new raster (coverage) layer in a specified workspace.

        Args:
            workspace (str): Name of the workspace where the layer will be created
            layer (CoverageModel): Model containing the raster layer configuration details,
                including metadata, native format, projection, and other coverage parameters

        Returns:
            GSResponse: Response object indicating success or failure
        """

        client = self.http_client
        response = client.post(
            f"/workspaces/{workspace}/coverages",
            data=layer.model_dump_json(),
            headers=self.headers,
        )
        return self.recognize_response(response.status_code)

    @exception_handler
    def delete_layer(self, workspace: str, layer: str) -> GSResponse:
        """
        Delete a layer from a specified workspace in GeoServer.

        Args:
            workspace (str): Name of the workspace containing the layer
            layer (str): Name of the layer to delete

        Returns:
            GSResponse: Response object indicating success or failure
        """

        client = self.http_client
        response = client.delete(f"layers/{workspace}:{layer}")
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_all_layer_groups(
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
            response = client.get(f"workspaces/{workspace}/layergroups")
        else:
            response = client.get("layergroups")
        if response.status_code == 200:
            return LayerGroupsModel.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_all_geofence_rules(self) -> Union[RulesResponse, GSResponse]:
        """
        Retrieve all GeoFence rules configured in GeoServer.

        Returns:
            Union[RulesResponse, GSResponse]: Either a list of all rules or an error response
                - RulesResponse: Contains a list of all GeoFence rules if successful
                - GSResponse: Error response if the request fails
        """

        client = self.http_client
        # Check if the geofence plugin exists
        module_check = self.check_modules("geofence")
        # If the module check fails, return the GSResponse directly
        if isinstance(module_check, GSResponse):
            return module_check
        # Make the HTTP request to fetch geofence rules
        response = client.get("geofence/rules/", headers={"Accept": "application/json"})
        if response.status_code == 200:
            return RulesResponse.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def get_geofence_rule(self, id: int) -> Union[GetRule, GSResponse]:
        """
        Retrieve a specific GeoFence rule by its ID from GeoServer.

        Args:
            id (int): The unique identifier of the GeoFence rule to retrieve

        Returns:
            Union[GetRule, GSResponse]: Either the requested rule or an error response
                - GetRule: The rule details if found
                - GSResponse: Error response if the request fails
        """

        client = self.http_client
        # Check if the geofence plugin exists
        module_check = self.check_modules("geofence")
        # If the module check fails, return the GSResponse directly
        if isinstance(module_check, GSResponse):
            return module_check
        response = client.get(
            f"geofence/rules/id/{id}", headers={"Accept": "application/json"}
        )
        if response.status_code == 200:
            return Rule.model_validate(response.json())
        return self.recognize_response(response.status_code)

    @exception_handler
    def create_geofence(self, rule: Rule) -> GSResponse:
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

        posting_rule = NewRule(Rule=rule)
        # Check if the geofence plugin exists
        module_check = self.check_modules("geofence")
        # If the module check fails, return the GSResponse directly
        if isinstance(module_check, GSResponse):
            return module_check
        client = self.http_client
        response = client.post(
            "geofence/rules",
            content=posting_rule.model_dump_json(),
            headers=self.headers,
        )
        return self.recognize_response(response.status_code)
