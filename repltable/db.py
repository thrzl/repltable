from urllib3 import PoolManager
from urllib3.response import HTTPResponse
from typing import Any, Dict, List, Optional
from orjson import loads, dumps
from os import environ


class Database:
    __slots__ = (
        "http",
        "db_url",
        "_cache"
    )
    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url or environ.get("REPLIT_DB_URL")
        if not self.db_url: raise ValueError("No db_url passed, and REPLIT_DB_URL wasn't found in env vars!")
        self.http = PoolManager()
        self._cache: Dict[str, str] = {}

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
        return self.req(path="?prefix=").data.decode().splitlines()

    def get(self, name: str):
        if name in self._cache:
            return self._cache[name]
        res = self.req(path=f"/{name}")
        if res.status == 404: return None
        r = res.data.decode()
        try:
            return loads(r)
        except:
            return r

    def set(self, name: str, value: Any):
        self.req("POST", "/", body=dumps({name: value}), headers={'Content-Type': "application/json"})
        self._cache[name] = value

    def delete(self, name: str):
        self.req("DELETE", f"/{name}")
        del self._cache[name]
