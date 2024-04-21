from typing import Dict, List, Optional, Any
from .db import Database
from .util import filter_list

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

    def drop(self) -> None:
        """Delete the current table."""
        self.db.delete(self.name)

class TableDatabase:
    __slots__ = ("db", "db_url", "_tcsize")

    def __init__(self, db_url: Optional[str] = None, table_cachesize: int = 25):
        self.db = Database(db_url)
        self.db_url = db_url
        self._tcsize = table_cachesize

    def __iter__(self):
        return (i for i in self.tables())

    def __getitem__(self, name: str):
        return self.get(name)

    def get(self, key: str) -> Table:
        """Get a table from the database.

        Args:
            key (str): the table to get.

        Returns:
            Table: the table object.
        """        
        if key not in self.tables():
            self.db.set(key, {})
        items: List[Dict[str, Any]] = self.db.get(key)  # type: ignore
        return Table(self.db, key, items or [])

    def tables(self):
        return self.db.list_keys()

    def drop(self, name: str):
        return self.db.delete(name)


