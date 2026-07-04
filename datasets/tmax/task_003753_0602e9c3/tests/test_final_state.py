# test_final_state.py
import os
import stat
import tarfile
import hashlib
import pytest

def test_cwe_file():
    path = "/home/user/cwe.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip().upper()
    assert "CWE-338" in content or "CWE-327" in content, f"Expected CWE-338 or CWE-327 in {path}, got '{content}'"

def test_vault_tar_exists_and_valid():
    path = "/home/user/vault.tar"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert tarfile.is_tarfile(path), f"File {path} is not a valid tar archive."

def test_vault_directory_and_contents():
    vault_dir = "/home/user/vault"
    assert os.path.isdir(vault_dir), f"Directory {vault_dir} does not exist."

    admin_key_path = os.path.join(vault_dir, "admin_key.pem")
    backup_key_path = os.path.join(vault_dir, "backup_key.pem")

    assert os.path.isfile(admin_key_path), f"Valid key {admin_key_path} was not extracted or was incorrectly deleted."
    assert not os.path.exists(backup_key_path), f"Corrupted key {backup_key_path} was not deleted."

def test_target_rsa_exists_and_matches():
    target_path = "/home/user/target_rsa"
    vault_dir = "/home/user/vault"
    admin_key_path = os.path.join(vault_dir, "admin_key.pem")

    assert os.path.isfile(target_path), f"File {target_path} does not exist."
    assert os.path.isfile(admin_key_path), f"Cannot verify {target_path} because {admin_key_path} is missing."

    with open(target_path, 'rb') as f1, open(admin_key_path, 'rb') as f2:
        assert f1.read() == f2.read(), f"Content of {target_path} does not match {admin_key_path}."

def test_target_rsa_permissions():
    target_path = "/home/user/target_rsa"
    assert os.path.isfile(target_path), f"File {target_path} does not exist."

    st = os.stat(target_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Permissions of {target_path} are {oct(perms)}, expected 0o600."

def test_target_rsa_matches_manifest():
    target_path = "/home/user/target_rsa"
    manifest_path = "/home/user/manifest.sha256"

    assert os.path.isfile(target_path), f"File {target_path} does not exist."
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    expected_hash = None
    with open(manifest_path, 'r') as f:
        for line in f:
            if "admin_key.pem" in line:
                expected_hash = line.split()[0].strip()
                break

    assert expected_hash is not None, "Could not find admin_key.pem hash in manifest."

    hasher = hashlib.sha256()
    with open(target_path, 'rb') as f:
        hasher.update(f.read())
    actual_hash = hasher.hexdigest()

    assert actual_hash == expected_hash, f"Hash of {target_path} ({actual_hash}) does not match manifest ({expected_hash})."