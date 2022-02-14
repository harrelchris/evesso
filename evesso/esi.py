import os
import time

from .authorize import get_auth_jwt
from .refresh import get_refresh_jwt
from .files import dump_jwt, load_jwt
from . import config


class Esi:
    def __init__(self, client_id: str = None, scope: str = None, callback_url: str = None, jwt_file_path: str = None):
        """The Esi object implements a controller for managing authorization
        for the Eve Online ESI API. The primary interaction a user has is the
        `header` property function. This function return an authorization header
        to be used when requesting authorization-walled ESI endpoints.

        Example:

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

        :param client_id: str Client ID associated with your application, found at https://developers.eveonline.com/applications
        :param scope: str a space-delimited string of scopes, found at https://developers.eveonline.com/applications
        :param callback_url: str path to accept callback from auth server, found at https://developers.eveonline.com/applications. Default and recommended value is https://localhost/callback/
        :param jwt_file_path: str path at which the jwt will be stored
        """

        self.client_id = client_id or os.getenv('CLIENT_ID')
        self.scope = scope or os.getenv('SCOPE')
        self.callback_url = callback_url or os.getenv('CALLBACK_URL') or config.DEFAULT_CALLBACK_URL
        self.jwt_file_path = jwt_file_path or os.getenv('JWT_FILE_PATH') or config.DEFAULT_JWT_PATH

        if not self.client_id:
            raise ValueError('CLIENT_ID is required but not provided')
        if not self.scope:
            raise ValueError('SCOPE is required but not provided')
        if not self.callback_url:
            raise ValueError('CALLBACK_URL is required but not provided')

        self.jwt = None

    def get_auth_header(self):
        """Get the JWT from the appropriate location and extract the access_token to use in the header.
        This method must be executed upon every use of the header to ensure the header is valid when used

        :return: dict Header dict containing authorization header
        """
        jwt = self.get_jwt()
        access_token = jwt.get('access_token')
        header = {
            'Authorization': f'Bearer {access_token}',
        }
        return header

    @property
    def header(self):
        """Update the auth header to accept compression.

        TODO add user agent string as well

        :return: dict Header dict containing authorization and compression headers
        """

        header = self.get_auth_header()
        header.update({'Accept-Encoding': 'gzip'})
        return header

    def get_jwt(self):
        """Retrieve the JWT from one of three locations, in order of latency:
            1. Current Esi object. JWT will exist on the object after authorization or first retrieval from file system
                This is the common case, so make it fast.
            2. The file system. The JWT will exist on the file system if the app has already been authorized.
                It may be expired though, so refresh it if needed, but store it on the object either way.
            3. The SSO server. The app has not yet been authorized and no JWT exists on the file system, so get one.

        :return: dict JWT received from authorization server containing access token and refresh token
        """

        # Check jwt stored on object first, and ensure at least 30 seconds left before it expires
        if self.jwt and self.jwt.get('expires_at') - 30 > time.time():
            # Current JWT is still valid. Use it.
            return self.jwt

        # Check if the jwt.json file exists. If not, authorize
        if not os.path.exists(self.jwt_file_path):
            jwt = get_auth_jwt(self.client_id, self.scope, self.callback_url)
            dump_jwt(self.jwt_file_path, jwt)
            self.jwt = jwt
            return jwt

        # jwt.json exists, so app is authorized. Use stored jwt if not expired, else refresh
        else:
            jwt = load_jwt(self.jwt_file_path)
            if jwt.get('expires_at') - 30 < time.time():
                refresh_token = jwt.get('refresh_token')
                new_jwt = get_refresh_jwt(self.client_id, self.scope, refresh_token)
                dump_jwt(self.jwt_file_path, new_jwt)
                self.jwt = new_jwt
                return new_jwt
            else:
                self.jwt = jwt
                return jwt
