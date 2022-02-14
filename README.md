# EveSSO

SSO Authorization for Eve Online.

## About

This library implements the native SSO authorization flow as described [here](https://docs.esi.evetech.net/docs/sso/native_sso_flow.html). EveSSO will perform the authorization process as needed, store your access and refresh tokens, and refresh your access token as needed. It will then provide the required header for your requests.

## Installation

```
pip install evesso
```

## Quickstart

```
from evesso import Esi
import requests

esi = Esi(
    client_id='1234567890asdfghjklqwertyuiop',
    callback_url='http://localhost/',
    scope='esi-characters.some_scope.v1 esi-characters.some_scope.v1'
)
response = requests.get(
    'https://esi.evetech.net/latest/markets/structures/SOME_STRUCTURE_ID/?datasource=tranquility',
    headers=esi.header
)
response.raise_for_status()
print(response.json())
```

### Using .env file

```
CLIENT_ID = 1234567890asdfghjklqwertyuiop
CALLBACK_URL = http://localhost/
SCOPE = esi-characters.some_scope.v1 esi-characters.some_scope.v1
```

Esi will check environment variables for credentials if not parameterized.

```
from evesso import Esi
from dotenv import load_dotenv
import requests

load_dotenv()

esi = Esi()
response = requests.get(
    'https://esi.evetech.net/latest/markets/structures/SOME_STRUCTURE_ID/?datasource=tranquility',
    headers=esi.header
)
response.raise_for_status()
print(response.json())
```

## Running on a remote machine

If you want to run your program on a remote server, first run it on a local machine with a web browser to create the `jwt.json` file. Then move the `jwt.json` to your project directory on the remote server. You will need to complete the authorization process with a web browser to get the initial token.