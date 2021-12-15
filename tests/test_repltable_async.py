from repltable import AsyncReplTable, AsyncTable
import pytest

db = AsyncReplTable(
    "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsImtpZCI6InByaW1hcnktMjAyMS0wOS0yNSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb25tYW4iLCJleHAiOjE2MzM4NTkxOTUsImlhdCI6MTYzMzc0NzU5NSwiZGF0YWJhc2VfaWQiOiJhNTgyY2MxZS03MmZhLTRiYTktYmE4YS1lMDEzMWJlYTM1NTMifQ.eqocDVtGo2rBRHLVsFzERRPu1ESvZwhO4KqeFIlT-5nQTTWJUOnpgIgknusVdTfLFkErg7yE84gz0TCr1S6T-A"
)


async def test_drop_all_iter():
    for i in await db.keys():
        t = db[i]
        await t.drop()
    assert [i for i in db] == []


async def test_get_table():
    table = await db["newtesttable"]
    assert isinstance(table, AsyncTable)


async def test_get_key():
    table = await db["newtesttable"]
    print(table.get(fdsfds=1))
    assert not table.get(id=231231)


async def test_drop_table():
    table = await db["newtesttable"]
    await table.drop()
    assert getattr(db, "newtesttable", None) is None


async def test_set_get():
    table = await db["things"]
    await table.insert(dict(name="test", value=1, id=2131))
    assert isinstance(table.get(id=2131), list) and (table.get(id=2131))[0]["name"] in [
        "test",
        "test2",
    ]
    assert table.get_one(id=2131)["name"] in ["test", "test2"]
    await table.update(dict(id=2131, name="test2"), id=2131)
    assert (
        isinstance(table.get(id=2131), list)
        and (table.get(id=2131))[0]["name"] == "test2"
    )
    assert table.get_one(id=2131)["name"] == "test2"
    await table.insert(dict(name="bar", value="baz"))
    await table.insert(dict(name="foo", value="bar"))
    await table.insert(dict(foo="bar", flob="baz"))
    print(table.get_one("bar"))
    assert len(table.get_one("bar")) == 2


async def test_drop_table_with_data():
    table = await db["things"]
    await table.insert(dict(name="test", value=1, id=2131))
    await table.insert(dict(name="test2", value=2, id=2132))
    await table.drop()
    assert getattr(db, "things", None) is None


async def test_delete():
    table = await db["things"]
    await table.insert(dict(name="test", value=1, id=2131))
    await table.insert(dict(name="test2", value=2, id=2132))
    await table.delete(id=2131)
    assert not table.get(id=2131)


async def drop_table_from_db():
    await db.drop("things")
    assert getattr(db, "things", None) is None
