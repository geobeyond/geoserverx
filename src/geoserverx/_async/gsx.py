from dataclasses import dataclass
import json
from urllib import response

from ..utils.http_client import AsyncClient
from ..utils.auth import GeoServerXAuth


@dataclass
class AsyncGeoServerX:
    """
    Async Geoserver client
    """

    username: str
    password: str
    url: str
    head = {"Content-Type": "application/json"}

    def __post_init__(self):
        self.http_client = AsyncClient(
            base_url=self.url,
            auth=(self.username, self.password),
        )

    async def __enter__(self) -> "AsyncGeoServerX":
        return self

    async def __exit__(self, exc_t, exc_v, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self.http_client.aclose()

    @staticmethod
    def from_auth(
        auth: GeoServerXAuth,
    ) -> "AsyncGeoServerX":
        return AsyncGeoServerX(auth.username, auth.password, auth.url)

    def response_recognise(self, r):
        resp = {"code": r.status_code}
        if r.status_code == 200:
            resp["result"] = r.json()
        elif r.status_code == 401:
            resp["error"] = "Unauthorized request"
        elif r.status_code == 500:
            resp["error"] = "Internal Server error"
        elif r.status_code == 404:
            resp["error"] = "Result not found"
        elif r.status_code == 201:
            resp["result"] = "Data added successfully"
        elif r.status_code == 409:
            resp["error"] = "Same data found"
        return resp

    # Get all workspaces
    async def get_all_workspaces(self):
        async with self.http_client as Client:
            responses = await Client.get(f"workspaces")
        results = self.response_recognise(responses)
        return results

    # Get specific workspaces
    async def get_workspaces(self, workspace):
        async with self.http_client as Client:
            responses = await Client.get(f"workspaces/{workspace}")
        results = self.response_recognise(responses)
        return results

    # Create workspace
    async def create_workspace(self, name, default=False, Isolated=False) -> dict:
        try:
            payload: str = json.dumps(
                {"workspace": {"name": name, "isolated": Isolated}}
            )
            async with self.http_client as Client:
                responses = await Client.post(
                    f"workspaces?default={default}", data=payload, headers=self.head
                )
            results = self.response_recognise(responses)
            return results
        except Exception as e:
            return {"reload error": str(e)}
