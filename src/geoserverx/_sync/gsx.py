from dataclasses import dataclass
import json
from re import L
from geoserverx.models.gs_response import GSResponse
from typing import Union
from geoserverx.utils.enums import GSResponse_enum
from geoserverx.utils.errors import GeoServerXError
from ..models.style import *
from ..models.workspace import *
from ..models.data_store import *
from ..models.coverages_store import *
from ..utils.services.datastore import *
from ..utils.http_client import SyncClient
from ..utils.auth import GeoServerXAuth

@dataclass
class SyncGeoServerX:
	"""
	Sync Geoserver client
	"""

	username: str
	password: str
	url: str
	head = {"Content-Type": "application/json"}

	def __post_init__(self):
		if not self.username and not self.password and not self.url:
			raise GeoServerXError(0, "Username, Password and URL is missing")
		elif not self.username or self.username == '' :
			raise GeoServerXError(0, "Username is missing")
		elif not self.password or self.password == '':
			raise GeoServerXError(0, "password is missing")
		elif not self.url or self.url == '':
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
		if r.status_code == 401:
			resp= GSResponse_enum._401.value
		elif r.status_code == 500:
			resp= GSResponse_enum._500.value
		elif r.status_code == 404:
			resp= GSResponse_enum._404.value
		elif r.status_code == 201:
			resp = GSResponse_enum._201.value
		elif r.status_code == 409:
			resp= GSResponse_enum._409.value
		return GSResponse.parse_obj(resp)

	# Get all workspaces
	def get_all_workspaces(self) -> Union[WorkspacesModel, GSResponse]:
		with self.http_client as Client:
			responses = Client.get(f"workspaces")
		if responses.status_code == 200:
			return WorkspacesModel.parse_obj(responses.json())
		else :
			results = self.response_recognise(responses)
			return results

	# Get specific workspaces
	def get_workspace(self, workspace: str) ->Union[WorkspaceModel, GSResponse]:
		with self.http_client as Client:
			responses = Client.get(f"workspaces/{workspace}")
		if responses.status_code == 200:
			return WorkspaceModel.parse_obj(responses.json())
		else :
			results = self.response_recognise(responses)
			return results

	# Create workspace
	def create_workspace(
		self, name: str, default: bool = False, Isolated: bool = False
	) -> GSResponse:
		try:
			payload: NewWorkspace = NewWorkspace(workspace=NewWorkspaceInfo(name=name,isolated=Isolated))
			with self.http_client as Client:
				responses = Client.post(
					f"workspaces?default={default}", data=payload.json(), headers=self.head
				)
			results = self.response_recognise(responses)
			return results
		except Exception as e:
			resp = {"code":500,"response":"Error in sending request"}
			return GSResponse.parse_obj(resp)

	# Get vector stores in specific workspaces
	def get_vector_stores_in_workspaces(self, workspace: str) -> DataStoresModel:
		with self.http_client as Client:
			responses = Client.get(f"workspaces/{workspace}/datastores")
		if responses.status_code == 200:
			return DataStoresModel.parse_obj(responses.json())
		else :
			results = self.response_recognise(responses)
			return results

	# Get raster stores in specific workspaces
	def get_raster_stores_in_workspaces(self, workspace: str) -> CoveragesStoresModel:
		with self.http_client as Client:
			responses = Client.get(f"workspaces/{workspace}/coveragestores")
		if responses.status_code == 200:
			return CoveragesStoresModel.parse_obj(responses.json())
		else :
			results = self.response_recognise(responses)
			return results

	# Get vecor store information in specific workspaces
	def get_vector_store(self, workspace: str, store: str) -> DataStoreModel:
		url = f"workspaces/{workspace}/datastores/{store}.json"
		with self.http_client as Client:
			responses = Client.get(url)
		if responses.status_code == 200:
			return DataStoreModel.parse_obj(responses.json())
		else :
			results = self.response_recognise(responses)
			return results

	# Get raster  store information in specific workspaces
	def get_raster_store(self, workspace: str, store: str) -> CoveragesStoreModel:
		url = f"workspaces/{workspace}/coveragestores/{store}.json"
		with self.http_client as Client:
			responses = Client.get(url)
		if responses.status_code == 200:
			return CoveragesStoreModel.parse_obj(responses.json())
		else :
			results = self.response_recognise(responses)
			return results

	# Get all styles in GS
	def get_allstyles(self) -> AllStylesModel:
		with self.http_client as Client:
			responses = Client.get(f"styles")
		if responses.status_code == 200:
			return AllStylesModel.parse_obj(responses.json())
		else :
			results = self.response_recognise(responses)
			return results

	# Get specific style in GS
	def get_style(self, style: str) -> StyleModel :
		with self.http_client as Client:
			responses = Client.get(f"styles/{style}.json")
		if responses.status_code == 200:
			return StyleModel.parse_obj(responses.json())
		else :
			results = self.response_recognise(responses)
			return results

	def create_file_store(self,workspace:str,store:str,file,type):
		service : AddDataStoreProtocol = CreateFileStore()

		if type == 'shapefile':
			service = ShapefileStore(service=service, file=file)	 
		elif type== 'gpkg':
			service = GPKGfileStore(service=service,file=file)
		service.addFile(self.http_client,workspace,store)
		
