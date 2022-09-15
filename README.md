![image](https://user-images.githubusercontent.com/73202594/190297553-a53dde72-e981-4a7a-8fb3-2b6face1b0da.png)
---
![PyPI - Downloads](https://img.shields.io/pypi/dm/repltable?style=for-the-badge)
![code style](https://img.shields.io/badge/code%20style-black-black?style=for-the-badge&logo=python)

this is a project is to make it so that you can have tables in the replit db.

the main annoyance (for me) with replit is that it reverts a lot of database file changes, which forces you to use the repl.it database. also, you can't group together keys, and it takes *FOREVER* to install, due to it installing flask, aiohttp and a ton of other things you don't need for the database.

## ⚙️ installation 
```bash
pip install repltable
```

## 🪴 usage
```python
# if you are using this on replit
from repltable import db

# or...
from repltable import Database
db = Database("https://kv.replit.com/v0/...")


# repltable databases work like a dictionary
db.get(foo='bar')
>>> [{'foo': 'bar'}]

# repltable auto-creates tables if they don't exist
db.insert(dict(foo='bar'))

# you can get one, or get all matching documents
db.get_one(foo='bar')
>>> {'foo': 'bar'}


# you can also group keys together
from repltable import TableDatabase

table = TableDatabase.get("users")
# from here, it behaves as a regular database

table.get(foo='bar')
>>> [{'foo': 'bar'}]

# repltable auto-creates tables if they don't exist
table.insert(dict(foo='bar'))

# you can get one, or get all matching documents
table.get_one(foo='bar')
>>> {'foo': 'bar'}
```
## ❓ why not just use replit-py?
well, my goal is to make it so that you can use repl.it databases without having to use replit-py. replit-py has **27** dependencies. repltable has **2**.

plus, repltable has more features:
- caching (auto-updates itself for accuracy!)
- groups of keys (named tables)
- uses more efficient queries (you can **filter** keys!)


## 👥 contributing
to contribute, fork the repo, make a branch, and send a pull request.

for local development, you can install the dependencies with poetry:
```bash
poetry install
```

## 📜 license
this project is licensed under the [mit](https://choosealicense.com/licenses/mit/) license.
