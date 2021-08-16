from repltable import Database, Table
from replit import Database as rdb

db = Database(rdb())


def test_get_table():
    table = db["newtesttable"]
    print(table)
    assert isinstance(table, Table)


def test_get_key():
    table = db["newtesttable"]
    print(table.get(fdsfds=1))
    assert not table.get(id=231231)


def test_drop_table():
    table = db["newtesttable"]
    table.drop()
    assert getattr(db, "newtesttable", None) is None


def test_set_get():
    table = db["things"]
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
    table.insert(dict(name="foo", value='bar'))
    table.insert(dict(name="bar", value='baz'))
    table.insert(dict(foo="bar", flob='baz'))
    print(table.get_one('bar'))
    assert len(table.get_one('bar')) == 2


def test_drop_table_with_data():
    table = db["things"]
    table.insert(dict(name="test", value=1, id=2131))
    table.insert(dict(name="test2", value=2, id=2132))
    table.drop()
    assert getattr(db, "things", None) is None


def test_delete():
    table = db["things"]
    table.insert(dict(name="test", value=1, id=2131))
    table.insert(dict(name="test2", value=2, id=2132))
    table.delete(id=2131)
    assert not table.get(id=2131)

def drop_table_from_db():
    db.drop('things')
    assert getattr(db, 'things', None) is None