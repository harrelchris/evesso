import base64
import hashlib
import json
import secrets
import urllib
import webbrowser

import requests


def store_jwt(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)


def generate_random_url_safe_string(byte_len=32):
    return base64.urlsafe_b64encode(secrets.token_bytes(byte_len))


def generate_challenge(verifier):
    m = hashlib.sha256()
    m.update(verifier)
    d = m.digest()
    return base64.urlsafe_b64encode(d).decode().replace("=", "")


def generate_auth_url(callback_url, client_id, scope, code_challenge):
    params = {
        "response_type": "code",
        "redirect_uri": callback_url,
        "client_id": client_id,
        "scope": scope,
        "state": '0000000000',
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }

    return f"https://login.eveonline.com/v2/oauth/authorize/?{urllib.parse.urlencode(params)}"


def get_code_param():
    return input("Paste the query string 'code' parameter here: ")


def authorize(callback_url, client_id, scope, headers, token_url):
    code_verifier = generate_random_url_safe_string()
    code_challenge = generate_challenge(code_verifier)
    auth_url = generate_auth_url(callback_url, client_id, scope, code_challenge)
    webbrowser.open(auth_url)
    auth_code = get_code_param()

    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": auth_code,
        "code_verifier": code_verifier
    }

    response = requests.post(token_url, data=data, headers=headers)
    return response.json()


# def refresh_access_token():
#     with open(file_path) as f:
#         jwt = json.load(f)
#         refresh_token = jwt.get('refresh_token')
#
#     url = "https://login.eveonline.com/v2/oauth/token"
#
#     data = {
#         'grant_type': 'refresh_token',
#         'refresh_token': refresh_token,
#         'client_id': CLIENT_ID,
#         'scope': SCOPE,
#     }
#
#     response = requests.post(url, data=data, headers=headers)
#     store_jwt(response.json())

def main():
    pass