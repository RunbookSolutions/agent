import unittest
from requests_mock import Mocker
from unittest.mock import patch, mock_open

from src.modules.auth.Auth import Auth

class AuthEnabledTestCases(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="[agent]\nbackend_url=mock://local\n[auth]\nclient_id=0000-000-0000-0000\n")
    def test_auth_requests_device_code_and_polls_for_authorization(self, mock_file_open):
        with Mocker() as mocker:
            # Set up a mock response for a specific URL
            mocker.post('mock://local/oauth/device/code', text='{"device_code": "device_code","user_code": "user_code","verification_uri": "verification_uri","expires_in": "expires_in"}', status_code=200)
            #mocker.post('mock://local/oauth/token', text='{"error": "authorization_pending"}', status_code=400)
            
            mocker.register_uri('POST',
                'mock://local/oauth/token',
                [
                    {
                        'text': '{"error": "authorization_pending"}',
                        'status_code': 400
                    },
                    {
                        'text': '{"access_token":"access_token","token_type":"token_type","expires_in":"expires_in","scope":"scope"}',
                        'status_code': 200
                    }
                ]
                
            )
        
            with patch('os.path.exists', return_value=True):
                auth = Auth(enabled=True)

            assert auth._client_id == "0000-000-0000-0000"

            expectedPostData = {
                'client_id': '0000-000-0000-0000',
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                'scope': ''
            }

            assert 3 == len(mocker.request_history)

            request = mocker.request_history[0]
            assert request.url == 'mock://local/oauth/device/code'
            assert request.json() == expectedPostData

            expectedPostData = {
                'client_id': '0000-000-0000-0000',
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                'device_code': 'device_code'
            }

            request = mocker.request_history[1]
            assert request.url == 'mock://local/oauth/token'
            assert request.json() == expectedPostData

            assert auth._device_code.device_code == "device_code"
            assert auth._device_code.user_code == "user_code"
            assert auth._device_code.verification_uri == "verification_uri"
            assert auth._device_code.expires_in == "expires_in"

            assert auth._access_token.access_token == "access_token"
            assert auth._access_token.token_type == "token_type"
            assert auth._access_token.expires_in == "expires_in"
            assert auth._access_token.scope == "scope"

            expectedHeaders = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer access_token'
            }

            assert expectedHeaders == auth.getHeaders()