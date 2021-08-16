# repltable

![PyPI - Downloads](https://img.shields.io/pypi/dm/repltable?style=for-the-badge)
![code style](https://img.shields.io/badge/code%20style-black-black?style=for-the-badge&logo=python)

this is a project is to make it so that you can have tables in the replit db.

the main annoyance (for me) with replit is that it reverts a lot of database file changes, which forces you to use the repl.it database.

## installation 
```bash
pip install repltable
```

## usage
```python
import repltable
from replit import db

database = repltable.Database(db)

# repltable databases work like a dictionary
database['table'].get(foo='bar')
>>> [{'foo': 'bar'}]

# repltable auto-creates tables if they don't exist
table = database['nonexistenttable']
table.insert(dict(foo='bar'))

# you can get one, or get all matching documents
table.get_one(foo='bar')
>>> {'foo': 'bar'}
```

## contributing
to contribute, fork the repo, make a branch, and send a pull request.

for local development, you can install the dependencies with poetry:
```bash
poetry install
```

## license
[MIT](https://choosealicense.com/licenses/mit/)
