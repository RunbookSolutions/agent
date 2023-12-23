import unittest
from unittest.mock import patch, mock_open

from src.modules.auth.Auth import Auth

class AuthDisabledTestCases(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="[agent]\nbackend_url=mock://local\n")
    def test_auth_sets_url_from_config_even_if_disabled(self, mock_file_open):
        with patch('os.path.exists', return_value=True):
            auth = Auth(enabled=False)

        assert auth._server_url == "mock://local"

    def test_auth_returns_content_type_header_even_if_disabled(self):
        auth = Auth(enabled=False)

        expectedHeaders = {
            'Content-Type': 'application/json'
        }

        assert expectedHeaders == auth.getHeaders()