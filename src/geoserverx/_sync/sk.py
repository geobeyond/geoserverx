from dataclasses import dataclass
from typing import Union
from geoserverx.utils.logger import std_out_logger
import logging
from .gsx import SyncGeoServerX,GeoServerXAuth
from geoserverx.utils.http_client import SyncClient
import json

# write class name sk and import SyncGeoServerX in 
class SK(SyncGeoServerX):
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
        self.http_client = SyncClient(
            base_url=self.url,
            auth=(self.username, self.password),
        )

    def __enter__(self) -> "SK":
        return self

    def __exit__(self, exc_t, exc_v, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self.http_client.aclose()
    
    @staticmethod
    def from_auth(
        auth: GeoServerXAuth,
    ) -> "SK":
        return SK(auth.username, auth.password, auth.url)

    
    def pg_to_layers(self, workspace: str, store:str):
        Client = self.http_client
        response = Client.get(f"workspaces/{workspace}/datastores/{store}/featuretypes.json?list=all")
        if response.status_code == 200:
            alllayers = response.json()['list']['string']
            layerresp = {}
            for layer in alllayers:
                payload = json.dumps({
                "featureType": {
                    "name": layer
                }
                })
                res = Client.post(
                    f"workspaces/{workspace}/datastores/{store}/featuretypes.json",
                    content=payload,
                    headers=self.head,
                )
                layerresp[layer]=self.response_recognise(res.status_code)
            return layerresp
        else:
            results = self.response_recognise(response.status_code)
            return results
