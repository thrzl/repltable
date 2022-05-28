from urllib3 import PoolManager, encode_multipart_formdata
from urllib3.response import HTTPResponse
from typing import Any, List, Optional
from orjson import loads, dumps
from os import environ


class RadReplitDB:
    __slots__ = (
        "http",
        "db_url"
    )
    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url or environ.get("REPLIT_DB_URL")
        if not self.db_url: raise ValueError("No db_url passed, and REPLIT_DB_URL wasn't found in env vars!")
        self.http = PoolManager()

    def req(
        self,
        method: str = "GET",
        path: str = "",
        fields: dict = {},
        **kwargs
    ) -> HTTPResponse:
        return self.http.request_encode_body(
            method, f"{self.db_url}{path}", fields=fields, **kwargs
        )

    def list_keys(self) -> List[str]:
        return str(self.req(path="?prefix=").data, 'utf-8').splitlines()

    def get(self, name: str):
        res = self.req(path=f"/{name}")
        r = res.data.decode('utf-8')
        if res.status == 404: return None
        try:
            return loads(r)
        except:
            return r

    def set(self, name: str, value: Any):
        self.req("POST", "/", body=dumps({name: value}), headers={'Content-Type': "application/json"})

    def delete(self, name: str):
        self.req("DELETE", f"/{name}")
