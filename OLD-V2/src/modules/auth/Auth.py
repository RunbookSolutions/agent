from configparser import ConfigParser
from modules.interfaces import AuthInterface

class Auth(AuthInterface):
    _enabled: bool
    _url: str
    _client_id: str

    def __init__(self, enabled: bool) -> None:
        self._enabled = enabled
        try:
            config = ConfigParser()
            config.read('config.ini')
            self._url = config['agent'].get('server_url')
            self._client_id = config['auth'].get('client_id')
        except Exception as e:
            # TODO: Check this to be logging not printing
            print(f"An error occurred: {str(e)}")
            self._url = "https://graphql.runbook.solutions"
            self._client_id = "DEFAULT_CLIENT_ID"

    def getHeaders(self) -> { str: str }:
        if not self._enabled:
            return