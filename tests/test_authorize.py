import urllib.parse

from evesso import authorize
from evesso.const import AUTH_URL

CLIENT_ID = 'abc123'
SCOPE = 'abc.abc.v1 def.def.v2'
CALLBACK_URL = 'http://localhost/callback123'
JWT_FILE_PATH = 'jwt.json'


def test_build_auth_url():
    code_verifier = authorize.generate_byte_string()
    url = authorize.build_auth_url(client_id=CLIENT_ID, scope=SCOPE, callback_url=CALLBACK_URL, code_verifier=code_verifier)
    parsed = urllib.parse.urlparse(url)
    assert parsed.scheme == 'https'
    assert parsed.netloc == 'login.eveonline.com'
    assert parsed.path == '/v2/oauth/authorize/'

    qs = urllib.parse.parse_qs(parsed.query)
    assert qs['response_type'] == ['code']
    assert qs['redirect_uri'] == ['http://localhost/callback123']
    assert qs['client_id'] == ['abc123']
    assert qs['scope'] == ['abc.abc.v1 def.def.v2']
    assert qs['code_challenge_method'] == ['S256']
    assert qs['code_challenge'] == [authorize.generate_challenge(code_verifier)]


def test_parse_callback_url():
    code = '1234abcd'
    state = 'efgh9876'
    callback_url = f'http://www.example.com/?code={code}&state={state}'
    query_string = authorize.parse_callback_url(callback_url)
    parsed_code = query_string.get('code')[0]
    parsed_state = query_string.get('state')[0]
    assert parsed_code == code
    assert parsed_state == state


def test_generate_challenge():
    verifier = b'abc123'
    assert authorize.generate_challenge(verifier) == 'bKE9UspwyIPg8LsQHkJaiehiTeUdstI5JZOvaoQRgJA'
