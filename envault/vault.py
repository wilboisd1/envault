"""Vault management: create, load, and persist encrypted vaults per project."""

import json
import os
from pathlib import Path

from envault.crypto import decrypt, encrypt, generate_salt

DEFAULT_VAULT_DIR = Path.home() / ".envault"
VAULT_FILE_NAME = "vault.enc"


def _vault_path(project: str, vault_dir: Path = DEFAULT_VAULT_DIR) -> Path:
    """Return the path to the vault file for a given project."""
    return vault_dir / project / VAULT_FILE_NAME


def vault_exists(project: str, vault_dir: Path = DEFAULT_VAULT_DIR) -> bool:
    """Check whether a vault exists for the given project."""
    return _vault_path(project, vault_dir).exists()


def create_vault(
    project: str,
    password: str,
    variables: dict[str, str] | None = None,
    vault_dir: Path = DEFAULT_VAULT_DIR,
) -> Path:
    """Create a new encrypted vault for the project.

    Args:
        project: Unique project name / identifier.
        password: Master password used to encrypt the vault.
        variables: Initial key-value pairs to store (optional).
        vault_dir: Base directory where vaults are stored.

    Returns:
        Path to the created vault file.

    Raises:
        FileExistsError: If a vault already exists for the project.
    """
    path = _vault_path(project, vault_dir)
    if path.exists():
        raise FileExistsError(f"Vault already exists for project '{project}': {path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(variables or {}).encode()
    salt = generate_salt()
    ciphertext = encrypt(payload, password, salt)
    path.write_bytes(ciphertext)
    return path


def load_vault(
    project: str,
    password: str,
    vault_dir: Path = DEFAULT_VAULT_DIR,
) -> dict[str, str]:
    """Decrypt and return the variables stored in a project vault.

    Raises:
        FileNotFoundError: If no vault exists for the project.
        ValueError: If the password is incorrect or data is corrupted.
    """
    path = _vault_path(project, vault_dir)
    if not path.exists():
        raise FileNotFoundError(f"No vault found for project '{project}': {path}")

    ciphertext = path.read_bytes()
    plaintext = decrypt(ciphertext, password)
    return json.loads(plaintext.decode())


def save_vault(
    project: str,
    password: str,
    variables: dict[str, str],
    vault_dir: Path = DEFAULT_VAULT_DIR,
) -> None:
    """Encrypt and persist an updated variables dict back to the vault."""
    path = _vault_path(project, vault_dir)
    if not path.exists():
        raise FileNotFoundError(f"No vault found for project '{project}': {path}")

    payload = json.dumps(variables).encode()
    salt = generate_salt()
    ciphertext = encrypt(payload, password, salt)
    path.write_bytes(ciphertext)
