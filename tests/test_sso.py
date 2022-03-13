import os

import pytest
from evesso.sso import SSO

CLIENT_ID = 'abc123'
SCOPE = 'abc.abc.v1 def.def.v2'
CALLBACK_URL = 'http://localhost/callback123'
JWT_FILE_PATH = 'jwt.json'


def test_error_unparameterized():
    with pytest.raises(ValueError):
        SSO()


def test_no_error_parameterized():
    assert SSO(
        client_id=CLIENT_ID,
        scope=SCOPE,
        callback_url=CALLBACK_URL,
        jwt_file_path=JWT_FILE_PATH,
    )


def test_creds_from_env():
    os.environ['CLIENT_ID'] = CLIENT_ID
    os.environ['SCOPE'] = SCOPE
    os.environ['CALLBACK_URL'] = CALLBACK_URL
    os.environ['JWT_FILE_PATH'] = JWT_FILE_PATH

    sso = SSO()

    assert sso.client_id == CLIENT_ID
    assert sso.scope == SCOPE
    assert sso.callback_url == CALLBACK_URL
    assert sso.jwt_file_path == JWT_FILE_PATH


def test_assert_parameter_unchanged():
    sso = SSO(
        client_id=CLIENT_ID,
        scope=SCOPE,
        callback_url=CALLBACK_URL,
        jwt_file_path=JWT_FILE_PATH,
    )

    assert sso.client_id == CLIENT_ID
    assert sso.scope == SCOPE
    assert sso.callback_url == CALLBACK_URL
    assert sso.jwt_file_path == JWT_FILE_PATH


def test_append_expiry():
    jwt = {'expires_in': 1199}
    jwt = SSO.append_jwt_expiry(jwt)
    assert jwt.get('expires_at', None)
