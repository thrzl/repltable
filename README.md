![image](https://user-images.githubusercontent.com/73202594/190297553-a53dde72-e981-4a7a-8fb3-2b6face1b0da.png)
---
![PyPI - Downloads](https://img.shields.io/pypi/dm/repltable?style=for-the-badge)
![code style](https://img.shields.io/badge/code%20style-black-black?style=for-the-badge&logo=python)

this is a better wrapper for the replit db built in to the platform. boating much higher performance and more features, repltable is the best way to interact with replit databases.

## ⚙️ installation 
```bash
pip install repltable
```

## 🪴 usage
```python
>>> from repltable import Database
>>> db = Database("https://kv.replit.com/v0/...")

# or on replit
>>> db = Database()

# regular key/value pairs
>>> db.get('bar')
"foo"

# set new values
>>> db.set("baz", "qux")
```
you can also group keys together as 'tables'. they're created on the fly if they don't already exist.
```py
>>> table = db.get_table("users")

# from here, you can filter rows by their attributes
>>> table.get(role='admin')
[{'username': 'thrzl', 'id': '1234', 'role': 'admin'}, ...]

# insert full rows at a time
>>> table.insert({'username': 'lzrht', 'id': '4321', 'role': 'member'})

# you can get one, or get all matching documents
>>> table.get_one(username='lzrht')
{'username': 'lzrht', 'id': '4321', 'role': 'member'}
```
## ❓ why not just use replit-py?
well, my goal is to make it so that you can use repl.it databases without having to use replit-py. replit-py has **27** dependencies. repltable has **1**.

repltable is also **significantly faster** than replit-py, thanks to it caching the keys in memory.

plus, repltable has more features:
- **local caching**, where the data is stored in memory as well as remotely
- **"table" support**
- **drop-in replacement** for replit-py's database


## 👥 contributing
to contribute, fork the repo, make a branch, and send a pull request.

for local development, you can install the dependencies with **[rye](rye-up.com)**:
```bash
rye sync
```

## 📜 license
this project is licensed under the [mit](https://choosealicense.com/licenses/mit/) license.
