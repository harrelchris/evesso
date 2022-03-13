import json
import os

from evesso.cache import Cache

PATH = 'file.extension'


def test_path():
    cache = Cache(path=PATH)
    assert cache.path == PATH


def test_dump():

    cache = Cache(path=PATH)
    jwt = {'this': 'that'}
    cache.dump(jwt)

    file = open(PATH, 'r')
    read_jwt = json.loads(file.read())
    file.close()
    os.remove(PATH)

    assert jwt == read_jwt


def test_load():
    cache = Cache(path=PATH)
    jwt = {'this': 'that'}
    cache.dump(jwt)
    read_jwt = cache.load()
    os.remove(PATH)
    assert jwt == read_jwt
