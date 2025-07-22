
import re
from typing import Annotated, Any, Dict, Literal

import requests
import urllib3
from pydantic import BaseModel, Field

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PbsServerConfig(BaseModel):
    server: str
    user: str
    token_id: str
    token_secret: str
    ignore_cert: Annotated[bool, Field(default=False)]


class PbsServer(PbsServerConfig):
    @property
    def auth(self):
        return f"PBSAPIToken={self.user}!{self.token_id}:{self.token_secret}"

    def _request_kwargs(self, url, params: Dict | None = None, data: Dict | None = None):

        url = re.sub(r"^/|//|/$", "", url)
        if not url.startswith("api2/json"):
            url = f"api2/json/{url}"

        kwargs: Dict[str, Any] = {
            "url": f"{self.server}/{url}",
            "headers": {"Authorization": self.auth},
            "verify": not self.ignore_cert,
        }

        if params:
            kwargs["params"] = params
        if data:
            kwargs["data"] = data

        return kwargs

    def get(self, url, params: Dict | None = None):
        kwargs = self._request_kwargs(url, params)
        return requests.get(**kwargs)

    def post(self, url, params: Dict | None = None, data: Dict | None = None):
        kwargs = self._request_kwargs(url, params, data)
        return requests.post(**kwargs)


BackupType = Literal["vm"] | Literal["ct"] | Literal["host"]


class BackupMetrics(BaseModel):
    store: str
    id: str
    type: BackupType
    last_finish_time: int
    size: int


def get_backup_metrics(pbs: PbsServer):
    response = pbs.get("admin/datastore")
    stores = response.json().get("data")
    store_names = [s["store"] for s in stores]

    for store_name in store_names:
        response = pbs.get(f"admin/datastore/{store_name}/groups")
        groups = response.json().get("data")
        for group in groups:

            response = pbs.get(f"admin/datastore/{store_name}/files", params={
                "backup-id": group.get("backup-id"),
                "backup-time": group.get("last-backup"),
                "backup-type": group.get("backup-type"),
            })

            files = response.json().get("data")
            size = sum([f["size"] for f in files if f["filename"] != "client.log.blob"])

            yield BackupMetrics(
                store=store_name,
                id=group.get("backup-id"),
                type=group.get("backup-type"),
                last_finish_time=group.get("last-backup"),
                size=size,
            )
