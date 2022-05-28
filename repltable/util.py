from typing import List

def remove_duplicates(data: list):
    if not data: return None
    return [dict(t) for t in {tuple(d.items()) for d in data}]

def filter_list(data: List[dict], **filters):
    if not data: return None
    l = []
    for i in data:
        for f in filters.items():
            if f in i.items():
                l.append(i)
    return l

