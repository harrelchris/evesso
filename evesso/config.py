import os

HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'login.eveonline.com'
}
AUTH_URL = 'https://login.eveonline.com/v2/oauth/authorize/'
TOKEN_URL = 'https://login.eveonline.com/v2/oauth/token'
DEFAULT_CALLBACK_URL = 'https://localhost/callback/'
STATE = os.getenv('STATE') or 'secret-state'
DEFAULT_JWT_PATH = 'jwt.json'
