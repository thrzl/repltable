from typing import List

def remove_duplicates(data: list):
    return list(set(data))

def filter_list(data: List[dict], **filters):
    l = []
    for i in data:
        for f in filters.items():
            if f in i.items():
                l.append(i)
    return l

