# EveSSO

SSO Authorization for Eve Online

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
    headers=esi.headers
)
response.raise_for_status()
database.store(response.json()
```

### .env File

```
CLIENT_ID = 1234567890asdfghjklqwertyuiop
CALLBACK_URL = http://localhost/
SCOPE = esi-characters.read_corporation_roles.v1
```