from __future__ import annotations
from httpx import Client, Response
from json import JSONDecodeError
from typing import Any, Dict, List, Optional, Union
from os import environ
from collections.abc import MutableMapping
from .util import filter_list


class Database:
    """The main class for interacting with the Replit Database.

    Args:
        db_url (Optional[str], optional): Your database URL. Defaults to None. If not supplied, it will attempt to get it from the environment variables.
        cache (MutableMapping, optional): The cache object to use. Should be dict-like (implement __setitem__ and __getitem__). Defaults to {}.
        preload_cache (bool, optional): Whether or not the database should populate the cache at startup. Can result in longer startups for large databases. Defaults to False.

    Raises:
        ValueError: If no db_url is passed and REPLIT_DB_URL is not found in the environment variables.
    """

    __slots__ = ("http", "db_url", "_cache")

    def __init__(
        self,
        db_url: Optional[str] = None,
        cache: MutableMapping = {},
        preload_cache: bool = False,
    ):
        self.db_url = db_url or environ.get("REPLIT_DB_URL")
        if not self.db_url:
            raise ValueError(
                "No db_url passed, and REPLIT_DB_URL wasn't found in env vars!"
            )
        self.http = Client(base_url=self.db_url)
        self._cache: MutableMapping[str, Any] = cache
        if preload_cache:
            for key in self.list_keys():
                self._cache[key] = self.get(key)

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
        return self.prefix("")

    def prefix(self, prefix: str) -> List[str]:
        """List all the keys in the database that start with a certain prefix.

        Args:
            prefix (str): the prefix to search for.

        Returns:
            List[str]: Every key in the database that starts with the prefix.
        """
        return self.req(path=f"?prefix={prefix}").text.splitlines()

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
        self.set_bulk({key: value})

    def set_bulk(self, data: Dict[str, Any]):
        """Set multiple values in the database.

        Args:
            data (Dict[str, Any]): the data to set in the database.
        """
        self.req(
            "POST",
            "/",
            json=str(data),
            headers={"Content-Type": "application/json"},
        )
        self._cache.update(data)

    def delete(self, key: str):
        """Delete a key from the database.

        Args:
            key (str): the key to delete from the database.
        """
        self.req("DELETE", f"/{key}")
        del self._cache[key]

    def get_table(self, table: str) -> Table:
        """Get a table from the database.

        Args:
            table (str): the table to get from the database.

        Raises:
            ValueError: if the table is not a valid table.

        Returns:
            List[Dict[str, Any]]: the table from the database.
        """
        if table not in self.list_keys():
            self.set(table, [])

        data = self.get(table)
        if isinstance(data, list):
            for i in data:
                if not isinstance(i, dict):
                    raise ValueError(f"`{table}` is not a valid table.")
        else:
            raise ValueError(f"`{table}` is not a valid table.")

        return Table(self, table, data or [])

    def list_tables(self) -> List[str]:
        """List all the tables from the database.

        Returns:
            List[str]: all the tables from the database.
        """
        data: List[str] = []
        keys = self.list_keys()
        for key in keys:
            if isinstance(key, list):
                for value in self.get(key):
                    if not isinstance(value, dict):
                        break
                data.append(key)

        return data


class Table:
    __slots__ = ("_cache", "db", "name", "data")
    """An object representing a table in the database.
    You should not need to create an instance of this class yourself.
    """

    def __init__(
        self,
        db: Database,
        name: str,
        data: List[Dict[str, Any]],
    ):
        self.db = db
        self.name = name
        self.data = data

    def __on_mutate(self):
        self.db.set(self.name, self.data)

    def delete(self, **filters) -> None:
        """Delete an existing document in the table.

        Args:
            **filters: Filters that the document must match.
        """
        self.data = [
            doc
            for doc in self.data
            if not any(doc.get(query, False) for query in filters)
        ]
        self.__on_mutate()

    def update(self, data: dict, **filters) -> None:
        """Update an existing document in the table.

        Args:
            data (dict): The new document data.
            **filters: Filters that the document must match.
        """
        for index, doc in enumerate(self.data):
            for query in filters:
                if doc.get(query, False):
                    self.data[index] = data

        self.__on_mutate()

    def get(self, *text, **filters) -> Optional[List[dict]]:
        """Gets all documents matching the given query.

        Args:
            *text: The text to search for in the documents.
            **filters: Filters that the document must match.

        Returns:
            List[dict]: Returns a list of documents matching the given query.
        """
        filtered = filter_list(self.data, **filters)

        if not (text or filters):
            return self.data
        return filtered

    def get_one(self, *args, **filters):
        """Gets the first document matching the given query.

        Args:
            *args: The text to search for in the documents.
            **filters: Filters that the document must match.

        Returns:
            dict: The document found.
        """
        if args and filters:
            raise ValueError("Both args or filters were passed!")
        try:
            return self.get(*args, **filters)[0]
        except IndexError:
            return None

    def insert(self, data: dict) -> None:
        """Insert a new document into the table.

        Args:
            data (dict): The data to insert.
        """
        if not isinstance(data, dict):
            raise TypeError("Data is not a dict object")
        self.data.append(data)
        self.__on_mutate()