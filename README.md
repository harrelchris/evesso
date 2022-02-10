# EVESSO

SSO Authorization library for requesting protected ESI routes for the Eve Online API

## Quickstart

```
from dotenv import load_dotenv
from evesso import ESI

load_dotenv()


esi = ESI()
data = esi.get('/characters/12345678/roles/')
print(data)
```
