"""Tests for envault.vault — vault lifecycle operations."""

import pytest

from envault.vault import create_vault, load_vault, save_vault, vault_exists

PROJECT = "test-project"
PASSWORD = "s3cr3tP@ss"


@pytest.fixture()
def tmp_vault_dir(tmp_path):
    return tmp_path


def test_vault_does_not_exist_initially(tmp_vault_dir):
    assert vault_exists(PROJECT, vault_dir=tmp_vault_dir) is False


def test_create_vault_returns_path(tmp_vault_dir):
    path = create_vault(PROJECT, PASSWORD, vault_dir=tmp_vault_dir)
    assert path.exists()


def test_vault_exists_after_creation(tmp_vault_dir):
    create_vault(PROJECT, PASSWORD, vault_dir=tmp_vault_dir)
    assert vault_exists(PROJECT, vault_dir=tmp_vault_dir) is True


def test_create_vault_raises_if_already_exists(tmp_vault_dir):
    create_vault(PROJECT, PASSWORD, vault_dir=tmp_vault_dir)
    with pytest.raises(FileExistsError, match="already exists"):
        create_vault(PROJECT, PASSWORD, vault_dir=tmp_vault_dir)


def test_load_vault_returns_empty_dict_by_default(tmp_vault_dir):
    create_vault(PROJECT, PASSWORD, vault_dir=tmp_vault_dir)
    data = load_vault(PROJECT, PASSWORD, vault_dir=tmp_vault_dir)
    assert data == {}


def test_create_and_load_vault_with_variables(tmp_vault_dir):
    variables = {"API_KEY": "abc123", "DEBUG": "true"}
    create_vault(PROJECT, PASSWORD, variables=variables, vault_dir=tmp_vault_dir)
    data = load_vault(PROJECT, PASSWORD, vault_dir=tmp_vault_dir)
    assert data == variables


def test_load_vault_raises_on_missing_vault(tmp_vault_dir):
    with pytest.raises(FileNotFoundError, match="No vault found"):
        load_vault("nonexistent", PASSWORD, vault_dir=tmp_vault_dir)


def test_load_vault_raises_on_wrong_password(tmp_vault_dir):
    create_vault(PROJECT, PASSWORD, variables={"X": "1"}, vault_dir=tmp_vault_dir)
    with pytest.raises(ValueError):
        load_vault(PROJECT, "wrongpassword", vault_dir=tmp_vault_dir)


def test_save_vault_updates_variables(tmp_vault_dir):
    create_vault(PROJECT, PASSWORD, variables={"A": "1"}, vault_dir=tmp_vault_dir)
    save_vault(PROJECT, PASSWORD, {"A": "1", "B": "2"}, vault_dir=tmp_vault_dir)
    data = load_vault(PROJECT, PASSWORD, vault_dir=tmp_vault_dir)
    assert data == {"A": "1", "B": "2"}


def test_save_vault_raises_on_missing_vault(tmp_vault_dir):
    with pytest.raises(FileNotFoundError):
        save_vault("ghost", PASSWORD, {"K": "V"}, vault_dir=tmp_vault_dir)


def test_save_vault_overwrites_previous_data(tmp_vault_dir):
    create_vault(PROJECT, PASSWORD, variables={"OLD": "value"}, vault_dir=tmp_vault_dir)
    save_vault(PROJECT, PASSWORD, {"NEW": "data"}, vault_dir=tmp_vault_dir)
    data = load_vault(PROJECT, PASSWORD, vault_dir=tmp_vault_dir)
    assert "OLD" not in data
    assert data["NEW"] == "data"
