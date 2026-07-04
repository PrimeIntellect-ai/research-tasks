# test_final_state.py

import os
import hashlib
import pytest

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_script_exists_and_uses_flock():
    script_path = "/home/user/config_backup.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "flock" in content, "The script must use 'flock' for file locking."
    assert "configs.lock" in content, "The script must lock /home/user/configs.lock."

def test_new_manifest_correctness():
    manifest_path = "/home/user/new_manifest.txt"
    assert os.path.isfile(manifest_path), f"New manifest {manifest_path} does not exist."

    expected_files = [
        "/home/user/configs/cache.conf",
        "/home/user/configs/db.conf",
        "/home/user/configs/web.conf"
    ]

    expected_lines = []
    for filepath in expected_files:
        assert os.path.isfile(filepath), f"Expected config file {filepath} is missing."
        checksum = get_sha256(filepath)
        expected_lines.append(f"{checksum}  {filepath}")

    expected_lines.sort()

    with open(manifest_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "The new manifest does not match the expected sorted checksums of regular files."

def test_backup_diff_contents():
    backup_dir = "/home/user/backup_diff"
    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} does not exist."

    backed_up_files = set(os.listdir(backup_dir))
    expected_files = {"web.conf", "cache.conf"}

    assert backed_up_files == expected_files, f"Backup directory should contain exactly {expected_files}, but found {backed_up_files}."

    for filename in expected_files:
        original = os.path.join("/home/user/configs", filename)
        backup = os.path.join(backup_dir, filename)

        assert get_sha256(original) == get_sha256(backup), f"Backed up file {filename} does not match the original."