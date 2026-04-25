"""Encryption and decryption utilities for envault vaults."""

import os
import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


SALT_SIZE = 16
ITERATIONS = 390_000


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    raw_key = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(raw_key)


def generate_salt() -> bytes:
    """Generate a cryptographically secure random salt."""
    return os.urandom(SALT_SIZE)


def encrypt(plaintext: str, password: str) -> bytes:
    """
    Encrypt a plaintext string with the given password.

    Returns salt + encrypted ciphertext as raw bytes.
    """
    salt = generate_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    ciphertext = fernet.encrypt(plaintext.encode("utf-8"))
    return salt + ciphertext


def decrypt(data: bytes, password: str) -> str:
    """
    Decrypt bytes previously produced by `encrypt`.

    Raises ValueError on wrong password or corrupted data.
    """
    salt = data[:SALT_SIZE]
    ciphertext = data[SALT_SIZE:]
    key = derive_key(password, salt)
    fernet = Fernet(key)
    try:
        plaintext = fernet.decrypt(ciphertext)
    except InvalidToken as exc:
        raise ValueError("Decryption failed: invalid password or corrupted vault.") from exc
    return plaintext.decode("utf-8")
