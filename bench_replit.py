from replit import db, Database  # type: ignore
from timeit import timeit

db: Database = db
db.set("test", "item")


def bench_replit():
    db.get("test")


print(timeit(bench_replit, number=10))

del db["test"]
