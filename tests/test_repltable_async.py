from repltable.asynchronous import Database, Table  # type: ignore
from dotenv import load_dotenv
from os import environ
import pytest

load_dotenv(".env.local")

if not environ.get("REPLIT_DB_URL"):
    pytest.exit("REPLIT_DB_URL not found.")


@pytest.fixture(scope="function")
def db():
    return Database(db_url=environ["REPLIT_DB_URL"])
# db = Database(db_url=environ["REPLIT_DB_URL"])

@pytest.mark.asyncio
async def test_drop_all_iter():
    for i in await db.keys():
        await db.delete(i)
    assert await db.keys() == []

@pytest.mark.asyncio
async def test_get_table():
    table = await db.get_table("newtesttable")
    print(table)
    assert isinstance(table, Table)

@pytest.mark.asyncio
async def test_get_key():
    table = await db.get_table("newtesttable")
    print(await table.get(fdsfds=1))
    assert not await table.get(id=231231)

@pytest.mark.asyncio
async def test_drop_table():
    await db.delete("newtesttable")
    assert await db.get("newtesttable") is None

@pytest.mark.asyncio
async def test_db_set_get():
    await db.set("test", "item")
    assert await db.get("test") == "item"
    await db.delete("test")
    assert await db.get("test") is None
    await db.set_bulk({"test": "item", "test2": "item2"})
    assert await db.get("test") == "item"
    assert await db.get("test2") == "item2"
    await db.delete("test")
    await db.delete("test2")

@pytest.mark.asyncio
async def test_set_get():
    table = await db.get_table("things")
    await table.insert(dict(name="test", value=1, id=2131))
    assert isinstance(await table.get(id=2131), list) and (await table.get(id=2131))[0][
        "name"
    ] in [
        "test",
        "test2",
    ]
    assert (await table.get_one(id=2131))["name"] in ["test", "test2"]
    await table.update(dict(id=2131, name="test2"), id=2131)
    assert (
        isinstance(await table.get(id=2131), list)
        and (await table.get(id=2131))[0]["name"] == "test2"
    )
    assert (await table.get_one(id=2131))["name"] == "test2"
    await table.insert(dict(name="foo", value="bar"))
    await table.insert(dict(name="bar", value="baz"))
    await table.insert(dict(foo="bar", flob="baz"))
    test_item = await table.get_one(foo="bar")
    assert (
        len(test_item.keys()) == 2
        and test_item["foo"] == "bar"
        and test_item["flob"] == "baz"
    )

@pytest.mark.asyncio
async def test_drop_table_with_data():
    table = await db.get_table("things")
    await table.insert(dict(name="test", value=1, id=2131))
    await table.insert(dict(name="test2", value=2, id=2132))
    await db.delete("things")
    assert getattr(db, "things", None) is None

@pytest.mark.asyncio
async def test_delete():
    table = await db.get_table("things")
    await table.insert(dict(name="test", value=1, id=2131))
    await table.insert(dict(name="test2", value=2, id=2132))
    await table.delete(id=2131)
    assert not await table.get(id=2131)

@pytest.mark.asyncio
async def drop_table_from_db():
    await db.delete("things")
    assert getattr(db, "things", None) is None
