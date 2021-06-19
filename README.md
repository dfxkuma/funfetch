# FunFetch
![PyPI](https://img.shields.io/pypi/v/funfetch?logo=pypi)
![PyPI - License](https://img.shields.io/pypi/l/funfetch)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Remote execution of a simple function on the server

All types of Python support objects.

## Installation

```bash
pip install funfetch
```
## Examples

Server
```py
from funfetch import Server

server = Server()

@server.use()
async def test(game: str, test):
    return f"play {game}! just {test}"

server.run()
```
Client
```py
from funfetch import Client
import asyncio

client = Client()

async def req():
    print(await client.test(game="testuser", test="test"))

asyncio.run(req())
```
