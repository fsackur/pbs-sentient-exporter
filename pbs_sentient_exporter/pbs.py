import re
from typing import Any, Dict

import requests
import urllib3
from pydantic import BaseModel

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PbsServer(BaseModel):
    server: str
    user: str
    token_id: str
    token_secret: str
    ignore_cert: bool

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
