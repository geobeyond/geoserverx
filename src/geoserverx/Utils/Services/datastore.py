import json
from logging import Logger
from typing import Protocol

from geoserverx.models.gs_response import GSResponse

import httpx
import httpx

class AddDataStoreProtocol(Protocol):
	"""
	Represents functionality of sending a file to the server.
	"""
	def addFile(
		self, client, workspace, store, method,
		store_payload, layer_payload, store_header,
		layer_header
	):
		...


class CreateFileStore:
	def addFile(
		self, client, workspace, store, method,
		store_payload, layer_payload, store_header,
		layer_header
	):
		try:
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
		except httpx.TimeoutException as exc:
			res = {}
			res['code'] = 504
			res['response'] = "Timeout Error"
			return GSResponse.parse_obj(res)
		except httpx.NetworkError as exc:
			res = {}
			res['code'] = 503
			res['response'] = "Geoserver unavailable"
			return GSResponse.parse_obj(res)


class ShapefileStore:
	def __init__(
		self,
		service: AddDataStoreProtocol,
		logger: Logger,
		file
	) -> None:
		self.inner = service
		self.logger = logger
		self.file = file

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
			client, workspace, store, "shp",
			store_payload, layer_payload,
			{"Content-Type": "application/json"},
			{"Content-Type": "application/zip"}
		)
		return result


class GPKGfileStore:
	def __init__(
		self,
		service: AddDataStoreProtocol,
		logger: Logger,
		file
	) -> None:
		self.inner = service
		self.logger = logger
		self.file = file

	def addFile(self, client, workspace, store):
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
		self.logger.debug(f"GeoPackage store payload: {store_payload}")
		layer_payload = self.file
		result = self.inner.addFile(
			client, workspace, store, "gpkg",
			store_payload, layer_payload,
			{"Content-Type": "application/json"},
			{"Content-Type": "application/json"}
		)
		return result
