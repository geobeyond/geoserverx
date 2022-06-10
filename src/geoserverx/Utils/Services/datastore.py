
   
import json
import time
from logging import Logger
from typing import Protocol


class AddDataStoreProtocol(Protocol):
    """
    Represents functionality of adding two numbers.
    """
    def addFile(self, client,  workspace, store, method, store_payload,layer_payload, store_header,layer_header):
        ...

class CreateFileStore:
    def addFile(self, client,  workspace, store, method, store_payload,layer_payload, store_header,layer_header):
        with client as Client:
            store_responses = Client.post(
                f"workspaces/{workspace}/datastores/", data=store_payload, headers=store_header
            )
            layer_responses = Client.put(
                f"workspaces/{workspace}/datastores/{store}/file.{method}",
                data=layer_payload,
                headers=layer_header,
            )
            results = layer_responses.status_code
            return results


class ShapefileStore:
    def __init__(self, service:AddDataStoreProtocol, file) -> None:
        self.inner = service
        self.file = file

    def addFile(self,client,workspace,store):
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
        print(store_payload)
        layer_payload = self.file
        result = self.inner.addFile(
            client,  workspace, store, "shp", store_payload,layer_payload, {"Content-Type": "application/json"}, {"Content-Type": "application/zip"}
        )
        return result


class GPKGfileStore:
    def __init__(self, service:AddDataStoreProtocol,file) -> None:
        self.inner = service
        self.file = file
    def addFile(self,client,workspace,store):
        store_payload: str = json.dumps(
            {
                "dataStore": {
                    "name": store,
                    "connectionParameters": {
                        "entry":  [
                            {"@key": "database", "$": "file:///path/to/nyc.gpkg"},
                            {"@key": "dbtype", "$": "geopkg"},
                        ]
                    },
                }
            }
        )
        print(store_payload)
        layer_payload = self.file
        result = self.inner.addFile(
            client,  workspace, store, "gpkg", store_payload,layer_payload, {"Content-Type": "application/json"}, {"Content-Type": "application/json"}
        )
        return result