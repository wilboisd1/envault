"""Tests for envault.crypto encryption/decryption utilities."""

import pytest
from envault.crypto import encrypt, decrypt, generate_salt, derive_key, SALT_SIZE


PASSWORD = "super-secret-password"
PLAINTEXT = "DATABASE_URL=postgres://user:pass@localhost/db"


def test_encrypt_returns_bytes():
    result = encrypt(PLAINTEXT, PASSWORD)
    assert isinstance(result, bytes)


def test_encrypted_length_greater_than_salt():
    result = encrypt(PLAINTEXT, PASSWORD)
    assert len(result) > SALT_SIZE


def test_decrypt_roundtrip():
    ciphertext = encrypt(PLAINTEXT, PASSWORD)
    recovered = decrypt(ciphertext, PASSWORD)
    assert recovered == PLAINTEXT


def test_different_encryptions_produce_different_ciphertext():
    """Each call should use a fresh salt, yielding different output."""
    c1 = encrypt(PLAINTEXT, PASSWORD)
    c2 = encrypt(PLAINTEXT, PASSWORD)
    assert c1 != c2


def test_wrong_password_raises_value_error():
    ciphertext = encrypt(PLAINTEXT, PASSWORD)
    with pytest.raises(ValueError, match="Decryption failed"):
        decrypt(ciphertext, "wrong-password")


def test_corrupted_data_raises_value_error():
    ciphertext = bytearray(encrypt(PLAINTEXT, PASSWORD))
    ciphertext[SALT_SIZE + 5] ^= 0xFF  # flip a byte in the ciphertext
    with pytest.raises(ValueError, match="Decryption failed"):
        decrypt(bytes(ciphertext), PASSWORD)


def test_generate_salt_length():
    salt = generate_salt()
    assert len(salt) == SALT_SIZE


def test_generate_salt_is_random():
    assert generate_salt() != generate_salt()


def test_derive_key_is_deterministic():
    salt = generate_salt()
    k1 = derive_key(PASSWORD, salt)
    k2 = derive_key(PASSWORD, salt)
    assert k1 == k2


def test_derive_key_differs_for_different_salts():
    k1 = derive_key(PASSWORD, generate_salt())
    k2 = derive_key(PASSWORD, generate_salt())
    assert k1 != k2


def test_encrypt_empty_string():
    ciphertext = encrypt("", PASSWORD)
    assert decrypt(ciphertext, PASSWORD) == ""
