from urllib3 import PoolManager
from cachetools import cached, TTLCache, LRUCache
from os import environ

class Database():
    def __init__(self, db_url: str = environ["REPLIT_DB_URL"], cachesize: int = 25):
        self.http = PoolManager()
        self._cache = LRUCache(cachesize)
        self.db_url = db_url

    def req(self, path: str="", method: str="GET", **params):
        return self.http.request(method, f"{self.db_url}{path}", fields=params)

    def __getitem__(self, name: str): 
        keys = http.get(self.db_url)

    def get(self, name: str):
        if name in (keys := tables()):
            return Table(name)
        else:
            raise AttributeError(f"No table named '{name}'")
        
    @cached(cache=TTLCache(1, 30))
    def tables(self):
        return self.req(prefix="")


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

