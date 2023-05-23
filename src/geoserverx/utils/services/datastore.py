import json
from logging import Logger
from typing import Protocol, Literal
from geoserverx.models.gs_response import GSResponse
import httpx


class AddDataStoreProtocol(Protocol):
    """
    Represents functionality of sending a file to the server.
    """

    def addFile(
        self,
        client,
        workspace,
        store,
        method,
        store_payload,
        layer_payload,
        store_header,
        layer_header,
    ):
        ...


class CreateFileStore:
    def addFile(
        self,
        client,
        workspace,
        store,
        method,
        store_payload,
        layer_payload,
        store_header,
        layer_header,
    ):
        store_responses = client.post(
            f"workspaces/{workspace}/datastores/",
            content=store_payload,
            headers=store_header,
        )
        layer_responses = client.put(
            f"workspaces/{workspace}/datastores/{store}/file.{method}",
            content=layer_payload,
            headers=layer_header,
        )
        result = store_responses.status_code
        return result


class ShapefileStore:
    def __init__(self, service: AddDataStoreProtocol, logger: Logger, file) -> None:
        self.inner = service
        self.logger = logger
        self.file = file
        self.result = None

    def addFile(self, client, workspace, store):
        store_payload: str = json.dumps(
            {
                "dataStore": {
                    "name": store,
                    "connectionParameters": {
                        "entry": [{"@key": "url", "$": f"file:{self.file}"}]
                    },
                }
            }
        )
        # self.logger.debug(f"Shapefile store payload: {store_payload}")
        layer_payload = self.file
        response = self.inner.addFile(
            client,
            workspace,
            store,
            "shp",
            store_payload,
            layer_payload,
            {"Content-Type": "application/json"},
            {"Content-Type": "application/zip"},
        )
        self.result = response
        return self.result


class GPKGfileStore:
    def __init__(self, service: AddDataStoreProtocol, logger: Logger, file) -> None:
        self.inner = service
        self.logger = logger
        self.file = file
        self.result = None

    def addFile(self, client, workspace, store):
        store_payload: str = json.dumps(
            {
                "dataStore": {
                    "name": store,
                    "connectionParameters": {
                        "entry": [
                            {"@key": "database", "$": f"file:{self.file}"},
                            {"@key": "dbtype", "$": "geopkg"},
                        ]
                    },
                }
            }
        )
        # self.logger.debug(f"GeoPackage store payload: {store_payload}")
        layer_payload = self.file
        response = self.inner.addFile(
            client,
            workspace,
            store,
            "gpkg",
            store_payload,
            layer_payload,
            {"Content-Type": "application/json"},
            {"Content-Type": "application/json"},
        )
        self.result = response
        return self.result
