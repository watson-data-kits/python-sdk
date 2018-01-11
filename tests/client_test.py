from functools import partial
import json
import time
from unittest.mock import patch

import pytest
from data_kits.client import Client
from data_kits.exceptions import InvalidApiKey, DataKitsException


class TestClient(object):
    def setup_method(self):
        Client.TOKEN_INFO = {}
        self.client = Client('api_key', 'url', '123')

    def test_api_url_no_trailing_slash(self):
        c = Client('key', 'url', '123', kit='test')
        assert c.base == 'url/test/v1'

    def test_api_url_trailing_slash(self):
        c = Client('key', 'url/', '123', kit='test')
        assert c.base == 'url/test/v1'

    def test_missing_api_key(self):
        with pytest.raises(TypeError):
            Client()

    def test_missing_api_url(self):
        with pytest.raises(TypeError):
            Client('key')

    def test_update_headers(self):
        self.client._update_headers('header', 'value')
        assert self.client.headers['header'] == 'value'

    @patch('requests.post')
    def test_fetch_token(self, patched_request):
        setattr(patched_request.return_value, 'json', lambda: {'access_token': 'token', 'expiration': 1})
        token_info = self.client._fetch_token()
        patched_request.assert_called_once() is True
        assert token_info['token'] == 'token'
        assert token_info['expires'] == 1

    @patch('requests.post')
    def test_fetch_token_error(self, patched_request):
        setattr(patched_request.return_value, 'json', lambda: {'errorMessage': 'error'})
        with pytest.raises(InvalidApiKey):
            self.client._fetch_token()

    def test_auth_header(self):
        self.client.TOKEN_INFO['token'] = 'token'
        header = self.client._auth_header()
        assert header == 'Bearer token'

    @patch('requests.get')
    def test_request_valid_token(self, patched_request):
        test_res = {'data': 'data'}
        params = {'param1': 'value'}
        self.client.TOKEN_INFO = {'token': 'token', 'expires': time.time() + 10}
        setattr(patched_request.return_value, 'json', lambda: test_res)
        setattr(patched_request.return_value, 'status_code', 200)
        res = self.client.request('endpoint', **params)
        patched_request.assert_called_with(
            '%s/endpoint' % self.client.base,
            headers=self.client.headers,
            params=params
        )
        assert res == test_res

    @patch('requests.get')
    def test_request_known_error(self, patched_request):
        test_res = {'error': 'error message'}
        params = {'param1': 'value'}
        self.client.TOKEN_INFO = {'token': 'token', 'expires': time.time() + 10}
        setattr(patched_request.return_value, 'json', lambda: test_res)
        setattr(patched_request.return_value, 'status_code', 400)
        with pytest.raises(DataKitsException) as e:
            self.client.request('endpoint', **params)
            patched_request.assert_called_with(
                '%s/endpoint' % self.client.base,
                headers=self.client.headers,
                params=params
            )
            assert e.message == test_res['error']

    @patch('requests.get')
    def test_request_unknown_error(self, patched_request):
        '''
        Tests when there is a bad request and requests.json() is not valid.

        1. Make sure that r.json() raises a JSONDecodeError
        2. Patch r.raise_for_status
        3. Assert that r.raise_for_status is called
        '''
        params = {'param1': 'value'}
        self.client.TOKEN_INFO = {'token': 'token', 'expires': time.time() + 10}
        setattr(patched_request.return_value, 'json', partial(json.loads, 'testing'))
        setattr(patched_request.return_value, 'raise_for_status', lambda: 'test')
        setattr(patched_request.return_value, 'status_code', 400)
        self.client.request('endpoint', **params)
        patched_request.assert_called_with(
            '%s/endpoint' % self.client.base,
            headers=self.client.headers,
            params=params
        )
        assert patched_request.raise_for_status.called_with()

    @patch('data_kits.client.Client._fetch_token')
    @patch('requests.get')
    def test_request_invalid_token(self, patched_request, token_patch):
        test_res = {'data': 'data'}
        params = {'param1': 'value'}
        setattr(patched_request.return_value, 'json', lambda: test_res)
        res = self.client.request('endpoint', **params)
        patched_request.assert_called_with(
            '%s/endpoint' % self.client.base,
            headers=self.client.headers,
            params=params
        )
        assert res == test_res
        token_patch.assert_called_once_with()

    def test_update_token(self):
        client_a = Client('api_key', 'url', '123')
        client_b = Client('api_key', 'url', '456')
        new_token = {'key': 'value'}
        Client._update_token(new_token)
        assert client_a.TOKEN_INFO == new_token
        assert client_a.TOKEN_INFO == client_b.TOKEN_INFO
