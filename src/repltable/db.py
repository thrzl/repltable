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
        """Underlying request method. The client's base url is set to `db_url`.

        Args:
            method (str, optional): The HTTP method to use. Defaults to "GET".
            path (str, optional): The path to send a request to. Defaults to "".
            headers (Dict[str, str], optional): The headers to include with the request. Defaults to {}.
            json (Optional[str], optional): the JSON body to send with the request. Defaults to None.

        Returns:
            Response: The returned HTTP response.
        """        
        return self.http.request(
            method=method, url=path, json=json, headers=headers, **kwargs
        )

    def list_keys(self) -> List[str]:
        """List all the keys in the database.

        Returns:
            List[str]: Every key in the database.
        """        
        return self.req(path="?prefix=").text.splitlines()

    def get(self, key: str) -> Union[Dict[str, Any], str, List[Dict[str, Any]], None]:
        """Get a value from the database.

        Args:
            key (str): the key to request from the database.

        Returns:
            Union[Dict[str, Any], str, List[Dict[str, Any]], None]: Either a dictionary, string, list of dictionaries, or None.
        """        
        if key in self._cache:
            return self._cache[key]
        res = self.req(path=f"/{key}")
        if res.status_code == 404:
            return None
        try:
            r = res.json()
        except JSONDecodeError:
            r = res.text
        return r

    def set(self, key: str, value: Any):
        """Set a value in the database.

        Args:
            name (str): the key to set in the database.
            value (Any): the value to set in the database.
        """        
        self.req(
            "POST",
            "/",
            json=str({key: value}),
            headers={"Content-Type": "application/json"},
        )
        self._cache[key] = value

    def delete(self, key: str):
        """Delete a key from the database.

        Args:
            key (str): the key to delete from the database.
        """        
        self.req("DELETE", f"/{key}")
        del self._cache[key]
