from runbooksolutions.store.Store import Store
import logging
import time
from typing import Optional

class AccessToken:

    def __init__(self, token_data: dict) -> None:
        try:
            self.access_token = token_data.get('access_token')
            self.token_type = token_data.get('token_type')
            self.expires_in = token_data.get('expires_in')
            self.scope = token_data.get('scope')
            self.creation_time = time.time()

            self._save_to_store()
        except AttributeError as e:
            logging.error(f"Failed to initialize AccessToken. Received data: {token_data}")
            logging.error(f"Error details: {e}")
            raise

    def _save_to_store(self) -> None:
        data_to_store = {
            'access_token': self.access_token,
            'token_type': self.token_type,
            'expires_in': self.expires_in,
            'scope': self.scope,
            'creation_time': self.creation_time
        }
        store = Store(self.__class__.__name__)
        store.save(data_to_store)

    @classmethod
    def load_from_store(cls) -> Optional['AccessToken']:
        store = Store(cls.__name__)
        data = store.load()

        if data:
            return cls(data)
        else:
            return None

    def getAccessToken(self) -> str:
        return self.access_token

    def getTokenType(self) -> str:
        return self.token_type

    def getExpiresIn(self) -> int:
        return self.expires_in

    def isExpired(self) -> bool:
        current_time = time.time()
        elapsed_time = current_time - self.creation_time
        return elapsed_time > self.expires_in
