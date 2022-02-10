import base64
import hashlib
import secrets
from urllib.parse import urlencode
import webbrowser

import requests

from .fileio import dump_jwt


class Auth:
    def __init__(self, jwt_file_path=None):
        self.auth_url = 'https://login.eveonline.com/v2/oauth/token'
        self.jwt_file_path = jwt_file_path or 'jwt.json'

    def get_code(self):
        return input("Paste code here: ")

    def authorize(self):
        code_verifier = generate_random_url_safe_string()
        query_string = {
            'response_type': 'code',
            'redirect_uri': 'http://localhost/',
            'client_id': '994916b9f0bb4048a901238d8f50b732',
            'scope': 'esi-characters.read_corporation_roles.v1',
            'code_challenge': generate_challenge(code_verifier),
            'code_challenge_method': 'S256',
            'state': 'something-unique'
        }
        webbrowser.open(f'https://login.eveonline.com/v2/oauth/authorize/?{urlencode(query_string)}')
        code = self.get_code()
        data = {
            "grant_type": "authorization_code",
            "client_id": '994916b9f0bb4048a901238d8f50b732',
            "code": code,
            "code_verifier": code_verifier
        }

        headers = {
            'Content - Type': 'application / x - www - form - urlencoded',
            'Host': 'login.eveonline.com'
        }
        response = requests.post(self.auth_url, data=data, headers=headers)
        jwt = response.json()
        dump_jwt(self.jwt_file_path, jwt)


def generate_random_url_safe_string(byte_len=32):
    return base64.urlsafe_b64encode(secrets.token_bytes(byte_len))


def generate_challenge(verifier):
    m = hashlib.sha256()
    m.update(verifier)
    d = m.digest()
    return base64.urlsafe_b64encode(d).decode().replace("=", "")
