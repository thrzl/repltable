from typing import List


def remove_duplicates(data: list):
    if not data:
        return None
    return [dict(t) for t in {tuple(d.items()) for d in data}]


def filter_list(data: List[dict], **filters: dict):
    if not data:
        return None
    return list(
        filter(lambda i: all(item in i.items() for item in filters.items()), data)
    )
