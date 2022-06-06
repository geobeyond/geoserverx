from dataclasses import dataclass
from geoserverx.utils.logger import std_out_logger
from geoserverx.models.style import *
from geoserverx.models.workspace import *
from geoserverx.models.data_store import *
from geoserverx.models.coverages_store import *
from geoserverx.utils.services.datastore import *
from geoserverx.utils.http_client import SyncClient
from geoserverx.utils.auth import GeoServerXAuth


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

	def response_recognise(self, r) -> dict:
		resp = {"code": r.status_code}
		if r.status_code == 200:
			resp["result"] = r.json()
		elif r.status_code == 401:
			resp= GSResponse._401.value
		elif r.status_code == 500:
			resp= GSResponse._500.value
		elif r.status_code == 404:
			resp= GSResponse._404.value
		elif r.status_code == 201:
			resp = GSResponse._201.value
		elif r.status_code == 409:
			resp= GSResponse._409.value
		return resp

	# Get all workspaces
	def get_all_workspaces(self) -> WorkspacesModel:
		with self.http_client as Client:
			responses = Client.get(f"workspaces")
		results = self.response_recognise(responses)
		return results

	# Get specific workspaces
	def get_workspaces(self, workspace: str) -> WorkspaceModel:
		with self.http_client as Client:
			responses = Client.get(f"workspaces/{workspace}")
		results = self.response_recognise(responses)
		return results

	# Create workspace
	def create_workspace(
		self, name: str, default: bool = False, Isolated: bool = False
	) -> dict:
		try:
			payload: NewWorkspace = NewWorkspace(workspace=NewWorkspaceInfo(name=name,isolated=Isolated))
			with self.http_client as Client:
				responses = Client.post(
					f"workspaces?default={default}", data=payload.json(), headers=self.head
				)
			results = self.response_recognise(responses)
			return results
		except Exception as e:
			return {"reload error": str(e)}

	# Get vector stores in specific workspaces
	def get_vector_stores_in_workspaces(self, workspace: str) -> DataStores:
		with self.http_client as Client:
			responses = Client.get(f"workspaces/{workspace}/datastores")
		results = self.response_recognise(responses)
		return results

	# Get raster stores in specific workspaces
	def get_raster_stores_in_workspaces(self, workspace: str) -> CoveragesStoresModel:
		with self.http_client as Client:
			responses = Client.get(f"workspaces/{workspace}/coveragestores")
		results = self.response_recognise(responses)
		return results

	# Get vecor store information in specific workspaces
	def get_vector_store(self, workspace: str, store: str) -> DataStore:
		url = f"workspaces/{workspace}/datastores/{store}.json"
		with self.http_client as Client:
			responses = Client.get(url)
		results = self.response_recognise(responses)
		return results

	# Get raster  store information in specific workspaces
	def get_raster_store(self, workspace: str, store: str) -> CoveragesStoreModel:
		url = f"workspaces/{workspace}/coveragestores/{store}.json"
		with self.http_client as Client:
			responses = Client.get(url)
		results = self.response_recognise(responses)
		return results

	# Get all styles in GS
	def get_allstyles(self) -> allStyles:
		with self.http_client as Client:
			responses = Client.get(f"styles")
		results = self.response_recognise(responses)
		return results

	# Get specific style in GS
	def get_style(self, style: str):
		with self.http_client as Client:
			responses = Client.get(f"styles/{style}.json")
		results = self.response_recognise(responses)
		return results

	def create_file_store(
		self,
		workspace:str,
		store:str,
		file,
		service_type
	):
		service : AddDataStoreProtocol = CreateFileStore()

		if service_type == 'shapefile':
			service = ShapefileStore(
				service=service, logger=std_out_logger("Shapefile"), file=file)
		elif service_type == 'gpkg':
			service = GPKGfileStore(
				service=service, logger=std_out_logger("GeoPackage"), file=file)
		else:
			raise ValueError(f"Service type {service_type} not supported")
		service.sync_addFile(self.http_client, workspace, store)
