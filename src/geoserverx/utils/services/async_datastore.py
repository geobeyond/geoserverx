import json
from logging import Logger
from typing import Protocol


class AddDataStoreProtocol(Protocol):
    """
    Represents functionality of sending a file to the server.
    """

    async def addFile(
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
    async def addFile(
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
        Client = client
        # async with client as Client:
        store_responses = await Client.post(
            f"workspaces/{workspace}/datastores/",
            data=store_payload,
            headers=store_header,
        )
        # async with client as Client:
        layer_responses = await Client.put(
            f"workspaces/{workspace}/datastores/{store}/file.{method}",
            content=layer_payload,
            headers=layer_header,
        )
        results = store_responses.status_code
        # await client.aclose()

        return results


class ShapefileStore:
    def __init__(
        self, service: AddDataStoreProtocol, logger: Logger, file, client
    ) -> None:
        self.inner = service
        self.logger = logger
        self.file = file
        self.client = client

    def addFile(self, client, workspace, store):
        store_payload: str = json.dumps(
            {
                "dataStore": {
                    "name": store,
                    "connectionParameters": {
                        "entry": [{"@key": "url", "$": "file:/path/to/nyc.shp"}]
                    },
                }
            }
        )
        self.logger.debug(f"Shapefile store payload: {store_payload}")
        layer_payload = self.file
        result = self.inner.addFile(
            self.client,
            workspace,
            store,
            "shp",
            store_payload,
            layer_payload,
            {"Content-Type": "application/json"},
            {"Content-Type": "application/zip"},
        )
        return result


class GPKGfileStore:
    def __init__(
        self, service: AddDataStoreProtocol, logger: Logger, file, client
    ) -> None:
        self.inner = service
        self.logger = logger
        self.file = file
        self.client = client

    def addFile(self, client, workspace, store):
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
        self.logger.debug(f"GeoPackage store payload: {store_payload}")
        layer_payload = self.file
        result = self.inner.addFile(
            self.client,
            workspace,
            store,
            "gpkg",
            store_payload,
            layer_payload,
            {"Content-Type": "application/json"},
            {"Content-Type": "application/json"},
        )
        return result
