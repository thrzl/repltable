from timeit import timeit
from repltable import Database


db = Database()
db.set("test", "item")


def bench_repltable():
    db.get("test")


print(timeit(bench_repltable, number=10))

db.delete("test")
