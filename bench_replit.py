from replit import db
from timeit import timeit

db.set("test", "item")


def bench_replit():
    db.get("test")


print(timeit(bench_replit, number=10))

del db["test"]
