from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from typing import Union, Any
from enum import Enum


class KeyType(Enum):
    PRIVATE = 'private'
    PUBLIC = 'public'


class CryptoUtils:

    @staticmethod
    def generate_rsa_key_pair() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=4096, 
            backend=default_backend()
        )

        public_key = private_key.public_key()
        return private_key, public_key
    

    @staticmethod
    def encrypt_data(data: bytes, public_key: rsa.RSAPublicKey) -> Union[bytes, None]:
        try:
            return public_key.encrypt(
                data, padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(), label=None)
                )
        except ValueError:
            return None
    

    @staticmethod
    def decrypt_data(encrypted_data: bytes, private_key: rsa.RSAPrivateKey) -> Union[bytes, None]:
        try:
            decrypted_data = private_key.decrypt(
                encrypted_data, padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(), label=None)
            )
            return decrypted_data
        except ValueError:
            return None


    @staticmethod
    def save_key_to_file(key, filename: str) -> None:
        if isinstance(key, rsa.RSAPrivateKey):
            key_bytes = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        elif isinstance(key, rsa.RSAPublicKey):
            key_bytes = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        else:
            raise ValueError("Unsupported key type")

        with open(filename, 'wb') as key_file:
            key_file.write(key_bytes)


    @staticmethod
    def load_key_from_file(filename: str, key_type: KeyType) -> Any:
        with open(filename, 'rb') as key_file:
            key_bytes = key_file.read()
            if key_type == KeyType.PRIVATE:
                return serialization.load_pem_private_key(
                    key_bytes, password=None, backend=default_backend())
            elif key_type == KeyType.PUBLIC:
                return serialization.load_pem_public_key(
                    key_bytes, backend=default_backend())
            
