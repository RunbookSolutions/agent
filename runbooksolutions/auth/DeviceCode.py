from runbooksolutions.store.Store import Store
import logging
import time

class DeviceCode:

    def __init__(self, DeviceCode: dict) -> None:
        self.device_code = DeviceCode["device_code"]
        self.user_code = DeviceCode["user_code"]
        self.verification_uri = DeviceCode["verification_uri"]
        self.expires_in = DeviceCode["expires_in"]
        self.creation_time = time.time()

        # Save the device code to the store
        self._save_to_store()

    def _save_to_store(self) -> None:
        data_to_store = {
            'device_code': self.device_code,
            'user_code': self.user_code,
            'verification_uri': self.verification_uri,
            'expires_in': self.expires_in,
            'creation_time': self.creation_time
        }
        store = Store(self.__class__.__name__)
        store.save(data_to_store)

    @classmethod
    def load_from_store(cls):
        store = Store(cls.__name__)
        data = store.load()

        if data:
            return cls(data)
        else:
            return None

    def getDeviceCode(self) -> str:
        return self.device_code
    
    def getUserCode(self) -> str:
        return self.user_code
    
    def getVerificationURI(self) -> str:
        return self.verification_uri
    
    def getExpiresIn(self) -> str:
        return self.expires_in
    
    def isExpired(self) -> bool:
        current_time = time.time()
        elapsed_time = current_time - self.creation_time
        return elapsed_time > self.expires_in
