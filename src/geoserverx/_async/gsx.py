from dataclasses import dataclass
from typing import Optional, Union

import httpx

from geoserverx.models.coverages_store import CoveragesStoreModel, CoveragesStoresModel
from geoserverx.models.data_store import (
    CreateDataStoreModel,
    CreateStoreItem,
    DataStoreModel,
    DataStoresModel,
    MainCreateDataStoreModel,
)
from geoserverx.models.geofence import NewRule, Rule, RulesResponse
from geoserverx.models.gs_response import GSResponse
from geoserverx.models.layer_group import LayerGroupsModel
from geoserverx.models.layers import LayerModel, LayersModel
from geoserverx.models.style import AllStylesModel, StyleModel
from geoserverx.models.workspace import (
    NewWorkspace,
    NewWorkspaceInfo,
    UpdateWorkspace,
    UpdateWorkspaceInfo,
    WorkspaceModel,
    WorkspacesModel,
)
from geoserverx.utils.auth import GeoServerXAuth
from geoserverx.utils.custom_exceptions import GSModuleNotFound
from geoserverx.utils.enums import GSResponseEnum
from geoserverx.utils.errors import GeoServerXError
from geoserverx.utils.http_client import AsyncClient
from geoserverx.utils.logger import std_out_logger
from geoserverx.utils.services.async_datastore import (
    AddDataStoreProtocol,
    CreateFileStore,
    GPKGfileStore,
    ShapefileStore,
)


@dataclass
class AsyncGeoServerX:
    """
    Async Geoserver client
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
        return GSResponse.model_validate(resp)

    # check if certain module/plugin exists in geoserver
    async def check_modules(self, name) -> Union[bool, GSResponse]:
        client = self.http_client
        try:
            response = await client.get("about/status.json")
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

    async def get_all_workspaces(self) -> Union[WorkspacesModel, GSResponse]:
        client = self.http_client
        response = await client.get("workspaces")
        if response.status_code == 200:
            return WorkspacesModel.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    async def get_workspace(self, workspace: str) -> Union[WorkspaceModel, GSResponse]:
        client = self.http_client
        response = await client.get(f"workspaces/{workspace}")
        if response.status_code == 200:
            return WorkspaceModel.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    async def delete_workspace(
        self, workspace: str, recurse: bool = False
    ) -> GSResponse:
        client = self.http_client
        response = await client.delete(
            f"workspaces/{workspace}", params={"recurse": recurse}
        )
        return self.response_recognise(response.status_code)

    async def create_workspace(
        self, name: str, default: bool = False, Isolated: bool = False
    ) -> GSResponse:
        client = self.http_client
        payload: NewWorkspace = NewWorkspace(
            workspace=NewWorkspaceInfo(name=name, isolated=Isolated)
        )
        response = await client.post(
            "workspaces",
            data=payload.model_dump_json(),
            headers=self.headers,
            params={"default": default},
        )
        return self.response_recognise(response.status_code)

    async def update_workspace(
        self, name: str, update: UpdateWorkspaceInfo
    ) -> GSResponse:
        client = self.http_client
        update_ws = UpdateWorkspace(workspace=update)
        response = await client.put(
            f"workspaces/{name}.json",
            data=update_ws.model_dump_json(exclude_none=True),
            headers=self.headers,
        )
        return self.response_recognise(response.status_code)

    async def get_vector_stores_in_workspaces(self, workspace: str) -> DataStoresModel:
        client = self.http_client
        response = await client.get(f"workspaces/{workspace}/datastores")
        if response.status_code == 200:
            return DataStoresModel.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    async def get_raster_stores_in_workspaces(
        self, workspace: str
    ) -> CoveragesStoresModel:
        client = self.http_client
        response = await client.get(f"workspaces/{workspace}/coveragestores")
        if response.status_code == 200:
            return CoveragesStoresModel.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    async def get_vector_store(self, workspace: str, store: str) -> DataStoreModel:
        url = f"workspaces/{workspace}/datastores/{store}.json"
        client = self.http_client
        response = await client.get(url)
        if response.status_code == 200:
            return DataStoreModel.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    async def get_raster_store(self, workspace: str, store: str) -> CoveragesStoreModel:
        url = f"workspaces/{workspace}/coveragestores/{store}.json"
        client = self.http_client
        response = await client.get(url)
        if response.status_code == 200:
            return CoveragesStoreModel.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    async def get_all_styles(self) -> AllStylesModel:
        client = self.http_client
        response = await client.get("styles")
        if response.status_code == 200:
            return AllStylesModel.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    async def get_style(self, style: str) -> StyleModel:
        client = self.http_client
        response = await client.get(f"styles/{style}.json")
        if response.status_code == 200:
            return StyleModel.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

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
                ).model_dump(exclude_none=True),
            )
        )
        client = self.http_client
        response = await client.post(
            f"workspaces/{workspace}/datastores/",
            data=payload.model_dump_json(),
            headers=self.headers,
        )
        return self.response_recognise(response.status_code)

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
        response = await service.addFile(self.http_client, workspace, store)
        return self.response_recognise(response)

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

    async def get_all_layers(
        self, workspace: Optional[str] = None
    ) -> Union[LayersModel, GSResponse]:
        client = self.http_client
        if workspace:
            response = await client.get(f"/workspaces/{workspace}/layers")
        else:
            response = await client.get("layers")
        if response.status_code == 200:
            return LayersModel.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    async def get_layer(
        self, workspace: str, layer: str
    ) -> Union[LayerModel, GSResponse]:
        client = self.http_client
        response = await client.get(f"layers/{workspace}:{layer}")
        if response.status_code == 200:
            return LayerModel.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    async def delete_layer(self, workspace: str, layer: str) -> GSResponse:
        client = self.http_client
        response = await client.delete(f"layers/{workspace}:{layer}")
        return self.response_recognise(response.status_code)

    async def get_all_layer_groups(
        self, workspace: Optional[str] = None
    ) -> Union[LayerGroupsModel, GSResponse]:
        client = self.http_client
        if workspace:
            response = await client.get(f"workspaces/{workspace}/layergroups")
        else:
            response = await client.get("layergroups")
        if response.status_code == 200:
            return LayerGroupsModel.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    # Reset geoserver
    async def reset_geoserver(self) -> GSResponse:
        """
        Resets all authentication, store, raster, and schema caches. This operation is used to force GeoServer to drop all caches and store connections and reconnect to each of them the next time they are needed by a request. This is useful in case the stores themselves cache some information about the data structures they manage that may have changed in the meantime.
        """
        Client = self.http_client
        responses = await Client.put(
            "/reset",
            headers=self.head,
        )
        results = self.response_recognise(responses.status_code)
        return results

    # Reload geoserver
    async def reload_geoserver(self) -> GSResponse:
        """
        Reloads the GeoServer catalog and configuration from disk. This operation is used in cases where an external tool has modified the on-disk configuration. This operation will also force GeoServer to drop any internal caches and reconnect to all data stores.
        """
        Client = self.http_client
        responses = await Client.put(
            "/reload",
            headers=self.head,
        )
        results = self.response_recognise(responses.status_code)
        return results

    # Get all geofence rules
    async def get_all_geofence_rules(self) -> Union[RulesResponse, GSResponse]:
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
            return RulesResponse.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    async def get_geofence_rule(self, id: int) -> Union[Rule, GSResponse]:
        client = self.http_client
        # Check if the geofence plugin exists
        module_check = await self.check_modules("geofence")
        # If the module check fails, return the GSResponse directly
        if isinstance(module_check, GSResponse):
            return module_check
        response = await client.get(
            f"geofence/rules/id/{id}", headers={"Accept": "application/json"}
        )
        if response.status_code == 200:
            return Rule.model_validate(response.json())
        else:
            return self.response_recognise(response.status_code)

    async def create_geofence(self, rule: Rule) -> GSResponse:
        PostingRule = NewRule(Rule=rule)
        # Check if the geofence plugin exists
        module_check = await self.check_modules("geofence")
        # If the module check fails, return the GSResponse directly
        if isinstance(module_check, GSResponse):
            return module_check
        client = self.http_client
        response = await client.post(
            "geofence/rules",
            content=PostingRule.model_dump_json(),
            headers=self.headers,
        )
        return self.response_recognise(response.status_code)
