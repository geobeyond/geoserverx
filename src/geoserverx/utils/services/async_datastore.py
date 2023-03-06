import json
from logging import Logger
from typing import Protocol
import asyncio

class AddDataStoreProtocol(Protocol):
    """
    Represents functionality of sending a file to the server.
    """
    async def addFile(
        self, client, workspace, store, method,
        store_payload, store_header,
        layer_header
    ):
        ...


class CreateFileStore:
    async def addFile(
        self, client, workspace, store, method,
        store_payload, store_header,
        layer_header
    ):
        async with client as Client:
            store_responses = await Client.post(
                f"workspaces/{workspace}/datastores/", data=store_payload, headers=store_header
            )
        return store_responses


class ShapefileStore:
    def __init__(
        self,
        service: AddDataStoreProtocol,
        logger: Logger,
        file,
        client
    ) -> None:
        self.inner = service
        self.logger = logger
        self.file = file
        self.client = client

    async def addFile(self,client, workspace, store):
        store_payload: str = json.dumps(
            {
                "dataStore": {
                    "name": store,
                    "connectionParameters": {
                        "entry": [{"@key": "url", "$": "file:"+self.file}]
                    },
                }
            }
        )
        # self.logger.debug(f"Shapefile store payload: {store_payload}")
        result = await self.inner.addFile(
            self.client, workspace, store, "shp",
            store_payload,
            {"Content-Type": "application/json"},
            {"Content-Type": "application/zip"}
        )
        return result


class GPKGfileStore:
    def __init__(
        self,
        service: AddDataStoreProtocol,
        logger: Logger,
        file,
        client
    ) -> None:
        self.inner = service
        self.logger = logger
        self.file = file
        self.client = client

    async def addFile(self, client, workspace, store):
        store_payload: str = json.dumps(
            {
                "dataStore": {
                    "name": store,
                    "connectionParameters": {
                        "entry":  [
                            {"@key": "database", "$": "file:"+self.file},
                            {"@key": "dbtype", "$": "geopkg"},
                        ]
                    },
                }
            }
        )
        # self.logger.debug(f"GeoPackage store payload: {store_payload}")
        result = await self.inner.addFile(
            self.client, workspace, store, "gpkg",
            store_payload,
            {"Content-Type": "application/json"},
            {"Content-Type": "application/json"}
        )
        return result
