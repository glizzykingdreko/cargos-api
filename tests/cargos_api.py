import sys
from pathlib import Path

# Ensure package import in test env without install
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

import base64
import types
import pytest

from cargos_api.api import CargosAPI
from cargos_api.exceptions import InvalidInput, InvalidResponse


def _valid_key() -> str:
    # 32 + 16 chars = 48
    return 'K'*32 + 'I'*16


def test_encrypt_key_length_validation():
    client = CargosAPI('user', 'pass', api_key='short')
    with pytest.raises(InvalidInput):
        client._encrypt_token_aes('token')


def test_auth_headers_format():
    client = CargosAPI('org-user', 'pass', api_key=_valid_key())
    # set token so _auth_headers won't call get_token
    client.token = {'access_token': 'TOKEN'}
    headers = client._auth_headers()
    assert headers['Organization'] == 'org-user'
    assert headers['Content-Type'] == 'application/json'
    assert headers['Authorization'].startswith('Bearer ')
    # Validate base64 shape
    enc = headers['Authorization'].split(' ', 1)[1]
    base64.b64decode(enc)


def test_get_token_invalid_response_raises(monkeypatch):
    client = CargosAPI('user', 'pass', api_key=_valid_key())

    class _Resp:
        def json(self):
            return {'errore': 'bad'}
    def fake_get(url, auth=None, timeout=None):
        return _Resp()

    monkeypatch.setattr('cargos_api.api.requests.get', fake_get)
    with pytest.raises(InvalidResponse):
        client.get_token()


def test_check_and_send_invalid_response_raises(monkeypatch):
    client = CargosAPI('user', 'pass', api_key=_valid_key())
    client.token = {'access_token': 'TOKEN'}

    class _Resp:
        def json(self):
            return {'errore': 'bad'}
    def fake_post(url, headers=None, json=None, timeout=None):
        return _Resp()

    monkeypatch.setattr('cargos_api.api.requests.post', fake_post)

    with pytest.raises(InvalidResponse):
        client.check_contracts(['X'])
    with pytest.raises(InvalidResponse):
        client.send_contracts(['X'])

