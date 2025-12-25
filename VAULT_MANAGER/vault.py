import json
import os
try:
    from VAULT_MANAGER.crypto_utils import derive_key, encrypt_data, decrypt_data
except Exception:
    try:
        from .crypto_utils import derive_key, encrypt_data, decrypt_data
    except Exception:
        from crypto_utils import derive_key, encrypt_data, decrypt_data

VAULT_FILE = "vault.enc"


def load_vault(master_password: str) -> dict:
    if not os.path.exists(VAULT_FILE):
        return {}

    with open(VAULT_FILE, "rb") as f:
        salt = f.read(16)
        encrypted = f.read()

    key = derive_key(master_password, salt)
    decrypted = decrypt_data(key, encrypted)
    return json.loads(decrypted.decode())


def save_vault(master_password: str, vault_data: dict):
    salt = os.urandom(16)
    key = derive_key(master_password, salt)
    data = json.dumps(vault_data).encode()
    encrypted = encrypt_data(key, data)

    with open(VAULT_FILE, "wb") as f:
        f.write(salt + encrypted)
