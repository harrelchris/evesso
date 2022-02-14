# EveSSO

SSO Authorization for Eve Online. EveSSO will perform the authorization process as needed, store your access and refresh tokens, and refresh your access token as needed. It will then provide the required header for your requests.

## Installation

```
pip install evesso
```

## Quickstart

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
database.store(response.json())
```

### .env File

```
CLIENT_ID = 1234567890asdfghjklqwertyuiop
CALLBACK_URL = http://localhost/
SCOPE = esi-characters.some_scope.v1 esi-characters.some_scope.v1
```