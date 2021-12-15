from typing import Any, List, Union, Dict
from replit import Database
from replit.database.database import AsyncDatabase


class ReplTable:
    def __init__(self, db_url: str):
        self._db = Database(db_url)

    def __iter__(self):
        return (self[table] for table in self._db.keys())

    def __setitem__(self, name: str, value) -> None:
        self._db[name] = value

    def __getitem__(self, key: str):
        if key not in self._db.keys():
            self._db[key] = []
        return Table(self._db[key], self, key)

    def __delattr__(self, name: str) -> None:
        if name in self._db.keys():
            del self._db[name]

    def drop(self, table: str):
        """Drops a table from the database.

        Parameters
        ----------
        table : str
            The name of the table to drop.
        """
        if table in self._db.keys():
            del self._db[table]


class Table:
    """An object representing a table in the database.

    You should not need to create an instance of this class yourself.
    """

    def __init__(self, docs: List[dict], db: Database, name: str):
        self._documents = docs
        self.db = db
        self.name = name

    def delete(self, **filters):
        """Delete an existing document in the table.

        Parameters
        ----------
        **filters
            Filters that the document must match.
        """
        for index, doc in enumerate(self._documents):
            for query, ans in filters.items():
                if query in doc and doc[query] == ans:
                    del self._documents[index]
        self.__update_changes()

    def update(self, data: dict, **filters):
        """Update an existing document in the table.

        Parameters
        ----------
        data : dict
            The new document data.
        **filters
            Filters that the document must match.
        """
        for index, doc in enumerate(self._documents):
            for query, ans in filters.items():
                if query in doc and doc[query] == ans:
                    self._documents[index] = data
        self.__update_changes()

    def __update_changes(self):
        self.db[self.name] = self._documents

    def __remove_duplicates(self, data: List[dict]):
        l = []  # type: List[dict]
        for i in data:
            if i not in l:
                l.append(i)
        return l

    def get(self, *text, **filters):
        """Gets all documents matching the given query.

        Returns
        -------
        list[dict]
            Returns a list of documents matching the given query.
        """
        l = []
        if text:
            for query in text:
                for doc in self._documents:
                    if query in doc.keys():
                        l.append(doc)
                    if query in doc.values():
                        l.append(doc)

        for i in self._documents:
            for key, value in filters.items():
                if i[key] == value:
                    l.append(i)
        if not any([text, filters]):
            return self._documents
        return self.__remove_duplicates(l)

    def get_one(self, *args, **filters):
        """Gets the first document matching the given query.

        Returns
        -------
        dict
            The document found.
        """
        if args and filters:
            raise ValueError("Both args or filters were passed!")
        try:
            return self.get(*args, **filters)[0]
        except IndexError:
            return None

    def insert(self, data: dict):
        """Insert a new document into the table.

        Parameters
        ----------
        data : dict
            A dictionary containing the data to insert.
        """
        self._documents.append(data)
        self.__update_changes()

    def drop(self):
        """Delete the current table."""
        delattr(self.db, self.name)


class AsyncReplTable:
    def __init__(self, db_url: str, cache={}):
        self._cache = cache
        self._db = AsyncDatabase(db_url)

    async def keys(self):
        return await self._db.keys()

    async def __getitem__(self, key: str):
        return await self.get_table(key)

    async def get_table(self, key: str):
        if key not in self._cache:
            self._cache[key] = await self._db.get(key)
        return AsyncTable(self._cache[key], self, key)

    async def drop(self, table: str):
        """Drops a table from the database.

        Parameters
        ----------
        table : str
            The name of the table to drop.
        """
        if table in self._db.keys():
            await self._db.delete(table)


class AsyncTable(Table):
    def __init__(self, docs: List[dict], db: AsyncReplTable, name: str):
        self._documents = docs
        self.db = db
        self.name = name

    async def drop(self):
        """Delete the current table."""
        await self.db._db.delete(self.name)
        del self.db._cache[self.name]

    async def __update_changes(self):
        await self.db.set(self.name, self._documents)
        self.db._cache[self.name] = self._documents

    async def delete(self, **filters):
        """Delete an existing document in the table.

        Parameters
        ----------
        **filters
            Filters that the document must match.
        """
        for index, doc in enumerate(self._documents):
            for query, ans in filters.items():
                if query in doc and doc[query] == ans:
                    del self._documents[index]
        await self.__update_changes()

    def get(self, *text, **filters) -> List[Dict[str, str]]:
        """Gets all documents matching the given query.

        Returns
        -------
        list[dict]
            Returns a list of documents matching the given query.
        """
        l = []
        if text:
            for query in text:
                for doc in self._documents:
                    if query in doc.keys():
                        l.append(doc)
                    if query in doc.values():
                        l.append(doc)

        for i in self._documents:
            for key, value in filters.items():
                if key in i and i[key] == value:
                    l.append(i)
        if not any([text, filters]):
            return self._documents
        return self.__remove_duplicates(l)

    async def update(self, data: dict, **filters):
        """Update an existing document in the table.

        Parameters
        ----------
        data : dict
            The new document data.
        **filters
            Filters that the document must match.
        """
        for index, doc in enumerate(self._documents):
            for query, ans in filters.items():
                if query in doc and doc[query] == ans:
                    self._documents[index] = data
        await self.__update_changes()

    def get_one(self, *args, **filters) -> Union[Dict[str, str], None]:
        """Gets the first document matching the given query.

        Returns
        -------
        dict
            The document found.
        """
        if args and filters:
            raise ValueError("Both args or filters were passed!")
        try:
            return self.get(*args, **filters)[0]
        except IndexError:
            return None

    async def insert(self, data: dict):
        """Insert a new document into the table.

        Parameters
        ----------
        data : dict
            A dictionary containing the data to insert.
        """
        self._documents.append(data)
        await self.__update_changes()
