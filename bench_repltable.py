from timeit import timeit
from repltable import Database  # type: ignore

db = Database()
db.set("test", "item")


def bench_repltable():
    db.get("test")


print(timeit(bench_repltable, number=100))

del db["test"]