from dataclasses import dataclass
from typing import Optional, Union

import httpx
from pydantic import ValidationError

from geoserverx.models.coverages_layer import CoverageModel
from geoserverx.models.coverages_store import CoveragesStoreModel, CoveragesStoresModel
from geoserverx.models.data_store import (
    CreateDataStoreModel,
    CreateStoreItem,
    DataStoreModel,
    DataStoresModel,
    MainCreateDataStoreModel,
)
from geoserverx.models.featuretypes_layer import FeatureTypesModel
from geoserverx.models.geofence import GetRule, NewRule, Rule, RulesResponse
from geoserverx.models.gs_response import GSResponse
from geoserverx.models.layer_group import LayerGroupsModel
from geoserverx.models.layers import LayerModel, LayersModel
from geoserverx.models.style import AllStylesModel, StyleModel
from geoserverx.models.workspace import (
    NewWorkspace,
    NewWorkspaceInfo,
    WorkspaceModel,
    WorkspacesModel,
)
from geoserverx.utils.auth import GeoServerXAuth
from geoserverx.utils.custom_exceptions import GSModuleNotFound
from geoserverx.utils.enums import GSResponseEnum
from geoserverx.utils.errors import GeoServerXError
from geoserverx.utils.http_client import SyncClient
from geoserverx.utils.logger import std_out_logger
from geoserverx.utils.services.datastore import (
    AddDataStoreProtocol,
    CreateFileStore,
    GPKGfileStore,
    ShapefileStore,
)


@dataclass
class SyncGeoServerX:
    """
    Sync Geoserver client
    """

    username: str = "admin"
    password: str = "geoserver"
    url: str = "http://127.0.0.1:8080/geoserver/rest/"
    headers = {"Content-Type": "application/json"}

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

    def __exit__(self, exc_t, exc_v, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self.http_client.aclose()

    @staticmethod
    def from_auth(
        auth: GeoServerXAuth,
    ) -> "SyncGeoServerX":
        return SyncGeoServerX(auth.username, auth.password, auth.url)

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
        elif r == 409:
            resp = GSResponseEnum._409.value
        elif r == 200:
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
        Client = self.http_client
        try:
            response = Client.get("about/status.json")
            response.raise_for_status()  # Raises an HTTPError for bad response (4xx and 5xx)

            # Extract and check the modules
            modules = [
                item["name"].lower() for item in response.json()["statuss"]["status"]
            ]
            if name.lower() in modules:
                return True
            else:
                # Raise exception if the plugin is not found
                raise GSModuleNotFound(f"'{name}' plugin not found")

        except httpx.HTTPStatusError as e:
            # Handle HTTP errors (e.g., 4xx, 5xx)
            return self.response_recognise(e.response.status_code)
        except httpx.RequestError as e:
            # Handle other request errors (e.g., network problems)
            return self.response_recognise(e.response.status_code)
        except GSModuleNotFound as e:
            # Handle Module not found exception
            return GSResponse(code=412, response=str(e))

    @exception_handler
    def get_all_workspaces(self) -> Union[WorkspacesModel, GSResponse]:
        Client = self.http_client
        response = Client.get("workspaces")
        if response.status_code == 200:
            return WorkspacesModel.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def get_workspace(self, workspace: str) -> Union[WorkspaceModel, GSResponse]:
        Client = self.http_client
        response = Client.get(f"workspaces/{workspace}")
        if response.status_code == 200:
            return WorkspaceModel.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def create_workspace(
        self, name: str, default: bool = False, Isolated: bool = False
    ) -> GSResponse:
        payload: NewWorkspace = NewWorkspace(
            workspace=NewWorkspaceInfo(name=name, isolated=Isolated)
        )
        Client = self.http_client
        response = Client.post(
            f"workspaces?default={default}",
            content=payload.model_dump_json(),
            headers=self.headers,
        )
        result = self.response_recognise(response.status_code)
        return result

    @exception_handler
    def get_vector_stores_in_workspaces(self, workspace: str) -> DataStoresModel:
        Client = self.http_client
        response = Client.get(f"workspaces/{workspace}/datastores")
        if response.status_code == 200:
            return DataStoresModel.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def get_raster_stores_in_workspaces(self, workspace: str) -> CoveragesStoresModel:
        Client = self.http_client
        response = Client.get(f"workspaces/{workspace}/coveragestores")
        if response.status_code == 200:
            return CoveragesStoresModel.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def get_vector_store(self, workspace: str, store: str) -> DataStoreModel:
        url = f"workspaces/{workspace}/datastores/{store}.json"
        Client = self.http_client
        response = Client.get(url)
        if response.status_code == 200:
            return DataStoreModel.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def create_vector_store(self, workspace: str, store: DataStoresModel) -> GSResponse:
        Client = self.http_client
        response = Client.post(
            f"workspaces/{workspace}/datastores",
            content=store.model_dump_json(),
            headers=self.headers,
        )
        result = self.response_recognise(response.status_code)
        return result

    @exception_handler
    def get_raster_store(self, workspace: str, store: str) -> CoveragesStoreModel:
        url = f"workspaces/{workspace}/coveragestores/{store}.json"
        Client = self.http_client
        response = Client.get(url)
        if response.status_code == 200:
            return CoveragesStoreModel.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def create_raster_store(
        self, workspace: str, store: CoveragesStoreModel
    ) -> GSResponse:
        Client = self.http_client
        response = Client.post(
            f"workspaces/{workspace}/coveragestores",
            content=store.model_dump_json(),
            headers=self.headers,
        )
        result = self.response_recognise(response.status_code)
        return result

    @exception_handler
    def delete_store(
        self, workspace: str, store: str, type: str
    ) -> GSResponse:  # TODO : add enum for type
        Client = self.http_client
        if type == "raster":
            response = Client.delete(
                f"/workspaces/{workspace}/coveragestores/{store}", headers=self.headers
            )
        elif type == "vector":
            response = Client.delete(
                f"/workspaces/{workspace}/datastores/{store}", headers=self.headers
            )
        result = self.response_recognise(response.status_code)
        return result

    @exception_handler
    def get_all_styles(self) -> AllStylesModel:
        Client = self.http_client
        response = Client.get("styles")
        if response.status_code == 200:
            return AllStylesModel.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def get_style(self, style: str) -> StyleModel:
        Client = self.http_client
        response = Client.get(f"styles/{style}.json")
        if response.status_code == 200:
            return StyleModel.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def create_file_store(
        self, workspace: str, store: str, file, service_type
    ) -> GSResponse:
        service: AddDataStoreProtocol = CreateFileStore()

        if service_type == "shapefile":
            service = ShapefileStore(
                service=service, logger=std_out_logger("Shapefile"), file=file
            )
        elif service_type == "gpkg":
            service = GPKGfileStore(
                service=service, logger=std_out_logger("GeoPackage"), file=file
            )
        else:
            raise ValueError(f"Service type {service_type} not supported")
        response = service.addFile(self.http_client, workspace, store)
        return self.response_recognise(response)

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
        Client = self.http_client
        response = Client.post(
            f"workspaces/{workspace}/datastores/",
            data=payload.model_dump_json(),
            headers=self.headers,
        )
        result = self.response_recognise(response.status_code)
        return result

    @exception_handler
    def get_all_layers(
        self, workspace: Optional[str] = None
    ) -> Union[LayersModel, GSResponse]:
        Client = self.http_client
        if workspace:
            response = Client.get(f"/workspaces/{workspace}/layers")
        else:
            response = Client.get("layers")
        if response.status_code == 200:
            return LayersModel.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def get_vector_layer(
        self, workspace: str, store: str, layer: str
    ) -> Union[FeatureTypesModel, GSResponse]:
        Client = self.http_client
        response = Client.get(
            f"/workspaces/{workspace}/datastores/{store}/featuretypes/{layer}.json"
        )
        if response.status_code == 200:
            try:
                return FeatureTypesModel.parse_obj(response.json())
            except ValidationError as validation_error:
                print("Pydantic Validation Error:")
                print(validation_error)
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def get_raster_layer(
        self, workspace: str, store: str, layer: str
    ) -> Union[CoverageModel, GSResponse]:
        Client = self.http_client
        response = Client.get(
            f"/workspaces/{workspace}/coveragestores/{store}/coverages/{layer}.json"
        )
        if response.status_code == 200:
            return CoverageModel.parse_obj(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def get_layer(
        self, workspace: str, layer: str, detail: bool = False
    ) -> Union[LayerModel, FeatureTypesModel, GSResponse]:
        Client = self.http_client
        response = Client.get(f"layers/{workspace}:{layer}")
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
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def create_vector_layer(
        self, workspace: str, layer: FeatureTypesModel
    ) -> GSResponse:
        Client = self.http_client
        response = Client.post(
            f"/workspaces/{workspace}/featuretypes",
            data=layer.model_dump(by_alias=True, exclude_none=True),
            headers=self.headers,
        )
        result = self.response_recognise(response.status_code)
        return result

    @exception_handler
    def create_raster_layer(self, workspace: str, layer: CoverageModel) -> GSResponse:
        Client = self.http_client
        response = Client.post(
            f"/workspaces/{workspace}/coverages",
            data=layer.model_dump_json(),
            headers=self.headers,
        )
        result = self.response_recognise(response.status_code)
        return result

    @exception_handler
    def delete_layer(self, workspace: str, layer: str) -> GSResponse:
        Client = self.http_client
        response = Client.delete(f"layers/{workspace}:{layer}")
        result = self.response_recognise(response.status_code)
        return result

    @exception_handler
    def get_all_layer_groups(
        self, workspace: Optional[str] = None
    ) -> Union[LayerGroupsModel, GSResponse]:
        Client = self.http_client
        if workspace:
            response = Client.get(f"workspaces/{workspace}/layergroups")
        else:
            response = Client.get("layergroups")
        if response.status_code == 200:
            return LayerGroupsModel.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def get_all_geofence_rules(self) -> Union[RulesResponse, GSResponse]:
        Client = self.http_client
        # Check if the geofence plugin exists
        module_check = self.check_modules("geofence")
        # If the module check fails, return the GSResponse directly
        if isinstance(module_check, GSResponse):
            return module_check
        # Make the HTTP request to fetch geofence rules
        response = Client.get("geofence/rules/", headers={"Accept": "application/json"})
        if response.status_code == 200:
            return RulesResponse.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def get_geofence_rule(self, id: int) -> Union[GetRule, GSResponse]:
        Client = self.http_client
        # Check if the geofence plugin exists
        module_check = self.check_modules("geofence")
        # If the module check fails, return the GSResponse directly
        if isinstance(module_check, GSResponse):
            return module_check
        response = Client.get(
            f"geofence/rules/id/{id}", headers={"Accept": "application/json"}
        )
        if response.status_code == 200:
            return Rule.model_validate(response.json())
        else:
            result = self.response_recognise(response.status_code)
            return result

    @exception_handler
    def create_geofence(self, rule: Rule) -> GSResponse:
        PostingRule = NewRule(Rule=rule)
        # Check if the geofence plugin exists
        module_check = self.check_modules("geofence")
        # If the module check fails, return the GSResponse directly
        if isinstance(module_check, GSResponse):
            return module_check
        Client = self.http_client
        response = Client.post(
            "geofence/rules",
            content=PostingRule.model_dump_json(),
            headers=self.headers,
        )
        result = self.response_recognise(response.status_code)
        return result
