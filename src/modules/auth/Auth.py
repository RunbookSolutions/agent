import configparser
import requests
import json

from src.interfaces.AuthInterface import AuthInterface

class DeviceCode:
    def __init__(self, raw_device_code: dict):
        self.device_code = raw_device_code.get('device_code')
        self.user_code = raw_device_code.get('user_code')
        self.verification_uri = raw_device_code.get('verification_uri')
        self.expires_in = raw_device_code.get('expires_in')

class AccessToken:
    def __init__(self, raw_access_token: dict):
        self.access_token = raw_access_token.get('access_token')
        self.token_type = raw_access_token.get('token_type')
        self.expires_in = raw_access_token.get('expires_in')
        self.scope = raw_access_token.get('scope')

class Auth(AuthInterface):
    _config: list
    _client_id: str
    _device_code: DeviceCode
    _access_token: AccessToken

    def __init__(self, enabled: bool) -> None:
        self._enabled = enabled

        self._config = configparser.ConfigParser()
        self._config.read('config.ini')
        self._server_url = self._config['agent']['backend_url']

        if self._enabled:
            self._client_id = self._config['auth']['client_id']
            self._getDeviceCode()
            self._pollForAuthorization()

    def getHeaders(self) -> { str, str }:
        headers = {
            'Content-Type': 'application/json'
        }
        if self._enabled:
            headers['Authorization'] = f'Bearer {self._access_token.access_token}'
        return headers
    
    def _getDeviceCode(self):
        data = {
            'client_id': self._client_id,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'scope': ''
        }

        response = requests.post(
            f"{self._server_url}/oauth/device/code", 
            json=data
        )
        self._device_code = DeviceCode(json.loads(response.text))

    def _pollForAuthorization(self):
        while True:
            data = {
                'client_id': self._client_id,
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                'device_code': self._device_code.device_code
            }

            response = requests.post(
                f"{self._server_url}/oauth/token", 
                json=data
            )

            if response.status_code == 200:
                self._access_token = AccessToken(json.loads(response.text))
                break
            else:
                continue

