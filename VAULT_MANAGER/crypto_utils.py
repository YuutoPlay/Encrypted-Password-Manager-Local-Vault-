import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type

SALT_SIZE = 16
KEY_SIZE = 32
NONCE_SIZE = 12


def derive_key(password: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=2,
        hash_len=KEY_SIZE,
        type=Type.ID
    )


def encrypt_data(key: bytes, data: bytes) -> bytes:
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return nonce + ciphertext


def decrypt_data(key: bytes, encrypted: bytes) -> bytes:
    aesgcm = AESGCM(key)
    nonce = encrypted[:NONCE_SIZE]
    ciphertext = encrypted[NONCE_SIZE:]
    return aesgcm.decrypt(nonce, ciphertext, None)
