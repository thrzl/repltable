from replit import db
from timeit import timeit

def bench_replit():
    db.get("amog")

print(timeit(bench_replit, number=10))