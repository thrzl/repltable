from timeit import timeit
from repltable import db

def bench_repltable():
    db.get("amog")

print(timeit(bench_repltable, number=10))