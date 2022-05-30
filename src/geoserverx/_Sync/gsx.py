from dataclasses import dataclass
import json
from urllib import response
from src.geoserverx.Utils.Model.Style import Style

from src.geoserverx.Utils.Model.Workspaces import Workspaces

from ..Utils.http_client import SyncClient
from ..Utils.auth import GeoServerXAuth
@dataclass
class SyncGeoServerX:
    """
    Sync Geoserver client
    """
    username : str 
    password : str 
    url : str
    head = {"Content-Type": "application/json"}

    def __post_init__(self):
        self.http_client = SyncClient(
            base_url=self.url,
            auth=(self.username,self.password),
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

    def response_recognise (self,r):
        resp = {"code":r.status_code}
        if r.status_code == 200:
            resp["result"]= r.json()
        elif r.status_code == 401:
            resp["error"] = "Unauthorized request"
        elif r.status_code == 500:
            resp["error"]= "Internal Server error"
        elif r.status_code == 404:
            resp["error"]= "Result not found"
        elif r.status_code == 201:
            resp["result"]= "Data added successfully"
        elif r.status_code == 409:
            resp["error"]= "Same data found"
        return  resp


    # Get all workspaces 
    def get_all_workspaces(self) -> Workspaces:
        with self.http_client as Client : 
            responses = Client.get(f'workspaces')
        results = self.response_recognise(responses)
        return results

    # Get specific workspaces 
    def get_workspaces(self, workspace:str) :
        with self.http_client as Client : 
            responses = Client.get(f'workspaces/{workspace}')
        results = self.response_recognise(responses)
        return results

    # Create workspace 
    def create_workspace(self, name:str, default:bool=False, Isolated:bool=False) -> dict:
        try:
            payload: str = json.dumps(
                {"workspace": {"name": name, "isolated": Isolated}}
            )
            with self.http_client as Client :
                    responses = Client.post(
                f"workspaces?default={default}", data=payload, headers=self.head
            )
            results = self.response_recognise(responses)
            return results
        except Exception as e:
            return {"reload error": str(e)}

    # Get vector stores in specific workspaces 
    def get_vector_stores_in_workspaces(self, workspace:str) :
        print((f'workspaces/{workspace}/datastores'))
        with self.http_client as Client : 
            responses = Client.get(f'workspaces/{workspace}/datastores')
        results = self.response_recognise(responses)
        return results

    # Get raster stores in specific workspaces 
    def get_raster_stores_in_workspaces(self, workspace:str) :
        with self.http_client as Client : 
            responses = Client.get(f'workspaces/{workspace}/coveragestores')
        results = self.response_recognise(responses)
        return results

    # Get raster stores in specific workspaces 
    def get_store_information(self,type:str, workspace:str,store:str) :
        if type=='vector':
            url = f'workspaces/{workspace}/datastores/{store}.json'
        elif type == 'raster':
            url = f'workspaces/{workspace}/coveragestores/{store}.json'
        else :
            return {'code': 500 , 'error': 'Please mention proper type'}
        with self.http_client as Client : 
            responses = Client.get(url)
        results = self.response_recognise(responses)
        return results

    # Get all styles in GS
    def get_allstyles(self) :
        with self.http_client as Client : 
            responses = Client.get(f'styles')
        results = self.response_recognise(responses)
        return results

    # Get specific style in GS
    def get_style(self, style:str) -> Style :
        with self.http_client as Client : 
            responses = Client.get(f'styles/{style}.json')
        results = self.response_recognise(responses)
        return results