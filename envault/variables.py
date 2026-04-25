"""High-level helpers for managing individual variables within a vault."""

from pathlib import Path

from envault.vault import DEFAULT_VAULT_DIR, load_vault, save_vault


def set_variable(
    project: str,
    password: str,
    key: str,
    value: str,
    vault_dir: Path = DEFAULT_VAULT_DIR,
) -> None:
    """Add or update a single variable in the project vault.

    Args:
        project: Project identifier.
        password: Master password for the vault.
        key: Environment variable name.
        value: Environment variable value.
        vault_dir: Base directory where vaults are stored.
    """
    variables = load_vault(project, password, vault_dir=vault_dir)
    variables[key] = value
    save_vault(project, password, variables, vault_dir=vault_dir)


def get_variable(
    project: str,
    password: str,
    key: str,
    vault_dir: Path = DEFAULT_VAULT_DIR,
) -> str:
    """Retrieve a single variable from the project vault.

    Raises:
        KeyError: If the variable does not exist in the vault.
    """
    variables = load_vault(project, password, vault_dir=vault_dir)
    if key not in variables:
        raise KeyError(f"Variable '{key}' not found in vault for project '{project}'.")
    return variables[key]


def delete_variable(
    project: str,
    password: str,
    key: str,
    vault_dir: Path = DEFAULT_VAULT_DIR,
) -> None:
    """Remove a variable from the project vault.

    Raises:
        KeyError: If the variable does not exist in the vault.
    """
    variables = load_vault(project, password, vault_dir=vault_dir)
    if key not in variables:
        raise KeyError(f"Variable '{key}' not found in vault for project '{project}'.")
    del variables[key]
    save_vault(project, password, variables, vault_dir=vault_dir)


def list_variables(
    project: str,
    password: str,
    vault_dir: Path = DEFAULT_VAULT_DIR,
) -> dict[str, str]:
    """Return all variables stored in the project vault."""
    return load_vault(project, password, vault_dir=vault_dir)
