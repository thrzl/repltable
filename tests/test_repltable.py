from repltable import Database, Table  # type: ignore
from dotenv import load_dotenv
from os import environ
import pytest

load_dotenv(".env.local")

if not environ.get("REPLIT_DB_URL"):
    pytest.exit("REPLIT_DB_URL not found.")

db = Database(db_url=environ["REPLIT_DB_URL"])


def test_drop_all_iter():
    for i in db.keys():
        db.delete(i)
    assert db.keys() == []


def test_get_table():
    table = db.get_table("newtesttable")
    print(table)
    assert isinstance(table, Table)


def test_get_key():
    table = db.get_table("newtesttable")
    print(table.get(fdsfds=1))
    assert not table.get(id=231231)


def test_drop_table():
    db.delete("newtesttable")
    assert db.get("newtesttable") is None


def test_db_set_get():
    db.set("test", "item")
    assert db.get("test") == "item"
    db.delete("test")
    assert db.get("test") is None
    db.set_bulk({"test": "item", "test2": "item2"})
    assert db.get("test") == "item"
    assert db.get("test2") == "item2"
    db.delete("test")
    db.delete("test2")


def test_set_get():
    table = db.get_table("things")
    table.insert(dict(name="test", value=1, id=2131))
    assert isinstance(table.get(id=2131), list) and (table.get(id=2131))[0]["name"] in [
        "test",
        "test2",
    ]
    assert table.get_one(id=2131)["name"] in ["test", "test2"]
    table.update(dict(id=2131, name="test2"), id=2131)
    assert (
        isinstance(table.get(id=2131), list)
        and (table.get(id=2131))[0]["name"] == "test2"
    )
    assert table.get_one(id=2131)["name"] == "test2"
    table.insert(dict(name="foo", value="bar"))
    table.insert(dict(name="bar", value="baz"))
    table.insert(dict(foo="bar", flob="baz"))
    assert len(table.get_one("bar")) == 2


def test_drop_table_with_data():
    table = db.get_table("things")
    table.insert(dict(name="test", value=1, id=2131))
    table.insert(dict(name="test2", value=2, id=2132))
    db.delete("things")
    assert getattr(db, "things", None) is None


def test_delete():
    table = db.get_table("things")
    table.insert(dict(name="test", value=1, id=2131))
    table.insert(dict(name="test2", value=2, id=2132))
    table.delete(id=2131)
    assert not table.get(id=2131)


def drop_table_from_db():
    db.delete("things")
    assert getattr(db, "things", None) is None
