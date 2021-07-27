from typing import List
from replit import Database as rdb
from replit import db


class Database:
    def __init__(self, database: rdb):
        self._db = database

    def __getitem__(self, key: str):
        if key not in self._db.keys():
            self._db[key] = []
        return Table(self._db[key], self, key)

    def __delattr__(self, name: str) -> None:
        if name in self._db.keys():
            del self._db[name]

    def drop(self, table: str):
        if table in self._db.keys():
            del self._db[table]


class Table:
    def __init__(self, docs: List[dict], db: Database, name: str):
        self._documents = docs
        self.db = db
        self.name = name

    def get(self, **kwargs):
        return [
            i
            for i in self._documents
            if (i[query] == ans for query, ans in kwargs.items())
        ]

    def get_one(self, **kwargs):
        return self.get(**kwargs)[0]

    def insert(self, data: dict):
        self._documents.append(data)

    def update(self, data: dict, **kwargs):
        for index, doc in enumerate(self._documents):
            for query, ans in kwargs.items():
                if doc[query] == ans:
                    self._documents[index] = data

    def drop(self):
        delattr(self.db, self.name)
