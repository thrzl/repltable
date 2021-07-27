# repltable

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

database['table'].get(foo='bar')
>>> [{'foo': 'bar'}, {'foo': 'baz'}]

table = database['nonexistenttable']
table.insert(dict(foo='bar'))

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