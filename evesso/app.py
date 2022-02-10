# TODO: store JWT on App object to avoid unnecessary file reads
# TODO: add type hints
# TODO: add comments
# TODO: decide how to complete authorization. Maybe CLI command using click?
# TODO: implement logging
# TODO: consider using sqlite db instead, or sqlalchemy
import os
import time

import requests

from .fileio import dump_jwt, load_jwt


class App:
    def __init__(self, client_id=None, scope=None, jwt_file_path=None):
        self.token_url = 'https://login.eveonline.com/v2/oauth/token'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'login.eveonline.com'
        }
        self.jwt_file_path = jwt_file_path or 'jwt.json'
        self.client_id = client_id or os.environ.get('CLIENT_ID')
        self.scope = scope or os.environ.get('SCOPE')

    def validate(self):
        if not self.client_id:
            raise ValueError('CLIENT_ID is required but missing')
        if not self.scope:
            raise ValueError('SCOPE is required but missing')

    def get_access_token(self):
        # TODO: optimize this process to remove multiple file calls. store on object
        jwt = load_jwt(self.jwt_file_path)
        if jwt.get('expires_at') < time.time():
            print('Access token is expired')
            refresh_token = jwt.get('refresh_token')
            self.refresh_access_token(refresh_token)
            jwt = load_jwt(self.jwt_file_path)
            return jwt.get('access_token')
        else:
            return jwt.get('access_token')

    def refresh_access_token(self, refresh_token):
        print('Refreshing access token')
        self.validate()
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'scope': self.scope,
        }

        response = requests.post(self.token_url, data=data, headers=self.headers)
        dump_jwt(self.jwt_file_path, response.json())
