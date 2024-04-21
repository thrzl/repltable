from httpx import Client, Response
from json import JSONDecodeError
from typing import Any, Dict, List, Optional, Union
from os import environ
from collections.abc import MutableMapping


class Database:
    __slots__ = ("http", "db_url", "_cache")

    def __init__(self, db_url: Optional[str] = None, cache: MutableMapping = {}):
        self.db_url = db_url or environ.get("REPLIT_DB_URL")
        if not self.db_url:
            raise ValueError(
                "No db_url passed, and REPLIT_DB_URL wasn't found in env vars!"
            )
        self.http = Client(base_url=self.db_url)
        self._cache: MutableMapping[str, str] = cache

    def req(
        self,
        method: str = "GET",
        path: str = "",
        headers: Dict[str, str] = {},
        json: Optional[str] = None,
        **kwargs,
    ) -> Response:
        return self.http.request(
            method=method, url=path, json=json, headers=headers, **kwargs
        )

    def list_keys(self) -> List[str]:
        return self.req(path="?prefix=").text.splitlines()

    def get(self, name: str) -> Union[Dict[str, Any], str, List[Dict[str, Any]], None]:
        if name in self._cache:
            return self._cache[name]
        res = self.req(path=f"/{name}")
        if res.status_code == 404:
            return None
        try:
            r = res.json()
        except JSONDecodeError:
            r = res.text
        return r

    def set(self, name: str, value: Any):
        self.req(
            "POST",
            "/",
            json=str({name: value}),
            headers={"Content-Type": "application/json"},
        )
        self._cache[name] = value

    def delete(self, name: str):
        self.req("DELETE", f"/{name}")
        del self._cache[name]
