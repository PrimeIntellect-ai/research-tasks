# test_final_state.py

import os
import json
import hashlib
import pytest

def compute_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def test_backup_destination_contents():
    inc_dir = "/home/user/backup_dest/inc_01"

    assert os.path.exists(inc_dir), f"Backup directory {inc_dir} does not exist"

    expected_files = [
        "file1.txt",
        "dirB/large1.dat",
        "dirB/large2.dat"
    ]

    for rel_path in expected_files:
        full_path = os.path.join(inc_dir, rel_path)
        assert os.path.isfile(full_path), f"Expected backed up file missing: {full_path}"

    unexpected_file = os.path.join(inc_dir, "dirA/file2.txt")
    assert not os.path.exists(unexpected_file), f"File {unexpected_file} should not have been copied (unchanged)"

def test_symlink_warnings_log():
    log_path = "/home/user/symlink_warnings.log"
    assert os.path.isfile(log_path), f"Symlink warnings log missing at {log_path}"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "Symlink warnings log is empty, expected loop detection warnings."

    # Check if the log contains indications of the A<->B loop
    loop_detected = any("link_to_A" in line or "link_to_B" in line for line in lines)
    assert loop_detected, "Symlink warnings log does not contain expected loop paths."

def test_new_manifest():
    manifest_path = "/home/user/backup_dest/manifest_01.json"
    assert os.path.isfile(manifest_path), f"New manifest missing at {manifest_path}"

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not valid JSON")

    base_dir = "/home/user/data_source"
    expected_keys = {
        "file1.txt",
        "dirA/file2.txt",
        "dirB/large1.dat",
        "dirB/large2.dat"
    }

    # Check that all expected keys are present
    manifest_keys = set(manifest.keys())
    assert expected_keys.issubset(manifest_keys), f"Manifest is missing keys. Expected {expected_keys}, found {manifest_keys}"

    # Verify the hashes match the actual files
    for rel_path in expected_keys:
        full_path = os.path.join(base_dir, rel_path)
        actual_hash = compute_sha256(full_path)
        assert manifest[rel_path] == actual_hash, f"Hash mismatch in manifest for {rel_path}. Expected {actual_hash}, got {manifest[rel_path]}"