import pickle
import hashlib
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.exceptions import InvalidTag

class Store:
    # Class variable for the encryption key (should be kept secure)
    STATIC_ENCRYPTION_KEY = None

    def __init__(self, filename):
        self.filename = "stores/" + filename + ".pkl"

    def _generate_checksum(self, data):
        # Calculate SHA-256 checksum for data
        hasher = hashlib.sha256()
        hasher.update(pickle.dumps(data))
        return hasher.hexdigest()

    def save(self, data):
        if not self.STATIC_ENCRYPTION_KEY:
            raise ValueError("Encryption key not set. Call set_encryption_key() before using the Store.")

        # Generate checksum
        checksum = self._generate_checksum(data)

        # Derive a key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=os.urandom(16),
            iterations=100000,
            length=32,
            backend=default_backend()
        )
        key = kdf.derive(self.STATIC_ENCRYPTION_KEY)

        # Generate a random IV for AES-CBC
        iv = os.urandom(16)

        # Pad the data to a multiple of the block size using PKCS7
        padder = PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(pickle.dumps(data)) + padder.finalize()

        # Encrypt the data using AES-CBC
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Save the data, key, IV, and checksum to the file
        with open(self.filename, 'wb') as file:
            file.write(key + iv + checksum.encode() + ciphertext)

    def load(self):
        try:
            # Read the data from the file
            with open(self.filename, 'rb') as file:
                encrypted_data = file.read()

            # Extract the salt from the end of the file
            key = encrypted_data[:32]
            encrypted_data = encrypted_data[32:]

            # Extract the IV, checksum, and ciphertext
            iv = encrypted_data[:16]
            checksum = encrypted_data[16:80].decode()
            ciphertext = encrypted_data[80:]

            # Decrypt the data using AES-CBC
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

            # Calculate the checksum of the decrypted data
            decrypted_checksum = self._generate_checksum(pickle.loads(decrypted_data))

            # Verify the checksum
            if checksum != decrypted_checksum:
                raise ValueError("Checksum verification failed. Data may be corrupted.")

            return pickle.loads(decrypted_data, fix_imports=False)

        except FileNotFoundError:
            return None

    @classmethod
    def set_encryption_key(cls, key):
        cls.STATIC_ENCRYPTION_KEY = key
