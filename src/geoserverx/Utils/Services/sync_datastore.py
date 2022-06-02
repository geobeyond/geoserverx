import json
import time
from logging import Logger
from typing import Protocol
from ..http_client import SyncClient


class AddDataStoreProtocol(Protocol):
    "Represents functionality of adding data to GS"

    def add(
        self,
        client: SyncClient,
        store_body: dict,
        workspace: str,
        store: str,
        method: str,
        file,
    ) -> int:
        ...


class AddService:
    "Implements AddDataStoreProtocol."

    def add(
        self,
        client: SyncClient,
        store_body: dict,
        workspace: str,
        store: str,
        method: str,
        file,

    ) -> int:
        with client as Client:
            responses = Client.post(
                f"workspaces/{workspace}/datastores/", data=store_body
            )
        results = responses.status_code()
        print(results)
        with client as Client:
            responses = Client.put(
                f"workspaces/{workspace}/datastores/{store}/file.{method}", data=file
            )
        results = responses.status_code()
        print(results)
        return results


class ShapeFileService:
    """
    Implements AddDataStoreProtocol. Sends Shapefile Zip to AddService.
    """

    def __init__(
        self,
        client,
        file,
        workspace,
        store,
        service: AddDataStoreProtocol,
    ) -> None:
        self._inner = service
        self.workspace = workspace
        self.store = store
        self.file = file
        self.client = client

    def add(self):
        store_payload: str = json.dumps(
            {
                "dataStore": {
                    "name": self.store,
                    "connectionParameters": {
                        "entry": [{"@key": "url", "$": "file:/path/to/nyc.shp"}]
                    },
                }
            }
        )
        print(store_payload)
        layer_payload: str = json.dumps(self.file)
        result = self._inner.add(
            self.client, store_payload, self.workspace, self.store, "shp", layer_payload
        )
        return result


class GPKGFileService:
    """
    Implements AddDataStoreProtocol. Sends GPKGfile Zip to AddService.
    """

    def __init__(
        self,
        service: AddDataStoreProtocol,
        file,
    ) -> None:
        self._inner = service

    def add(self, client: SyncClient, workspace: str, store: str, method: str, file):
        store_payload: str = json.dumps(
            {
                "dataStore": {
                    "name": store,
                    "connectionParameters": {
                        "entry": [
                            {"@key": "database", "$": "file:///path/to/nyc.gpkg"},
                            {"@key": "dbtype", "$": "geopkg"},
                        ]
                    },
                }
            }
        )
        layer_payload: str = json.dumps(file)
        result = self._inner.add(
            client, store_payload, workspace, store, "gpkg", layer_payload
        )
        print(result)
        return result
