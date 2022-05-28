from urllib3 import PoolManager
from urllib3.response import HTTPResponse
from typing import Any, List, Union
from orjson import loads


class RadReplitDB:
    __slots__ = (
        "http",
        "db_url"
    )
    def __init__(self, db_url: str):
        self.http = PoolManager()
        self.db_url = db_url

    def req(
        self,
        method: str = "GET",
        path: str = "",
        fields: dict = {},
        **kwargs
    ) -> HTTPResponse:
        return self.http.request(
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
        self.req("POST", "/{name}={value}", body=f"{name}={value}")

    def delete(self, name: str):
        self.req("DELETE", f"/{name}")
