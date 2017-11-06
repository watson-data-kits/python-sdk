import json
import time

import requests

from .exceptions import InvalidApiKey, KnowledgeKitsException


class Client(object):
    IAM_URL = 'https://iam.bluemix.net/oidc/token'
    TOKEN_INFO = {}

    def __init__(self, api_key, api_url, instance_id, kit='', version='v1'):
        self.api_key = api_key
        self.base = '%s/%s/%s' % (api_url.rstrip('/'), kit, version)
        self.headers = {'Instance-ID': instance_id}

    def _update_headers(self, header, value):
        self.headers.update({header: value})

    @classmethod
    def _update_token(cls, token_info):
        '''
        Updates token information for all instances of the Client
        '''
        cls.TOKEN_INFO = token_info

    def _fetch_token(self):
        data = {
            'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
            'apikey': self.api_key
        }
        r = requests.post(self.IAM_URL, data=data)
        data = r.json()
        if 'errorMessage' in data:
            raise InvalidApiKey(data['errorMessage'])
        token_info = {'token': data['access_token'], 'expires': data['expiration']}
        return token_info

    def _auth_header(self):
        return 'Bearer %s' % self.TOKEN_INFO.get('token')

    def request(self, endpoint, **params):
        """
        Makes a request and returns data.
        """

        # Check if the auth token is still valid and fetch a new one if not before making the request.
        if not self.TOKEN_INFO or time.time() > self.TOKEN_INFO.get('expires', 0):
            token_info = self._fetch_token()
            Client._update_token(token_info)
            self._update_headers('Authorization', self._auth_header())
        url = '%s/%s' % (self.base, endpoint)
        r = requests.get(url, headers=self.headers, params=params)

        data = None
        if r.status_code == 200:
            # Return the data if everything looks good
            data = r.json()
        else:
            try:
                # Check if our api returned an error message and raise exception with that message.
                data = r.json()
                if 'error' in data:
                    error_msg = data['error']
                    raise KnowledgeKitsException(error_msg)
            except json.JSONDecodeError:
                # Raise the uncaught exception
                r.raise_for_status()
        return data
