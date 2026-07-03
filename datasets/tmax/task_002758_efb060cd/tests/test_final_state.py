# test_final_state.py
import os
import hashlib
import pytest

def test_manifest_exists():
    manifest_path = '/home/user/valid_backups.manifest'
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

def test_manifest_contents():
    manifest_path = '/home/user/valid_backups.manifest'
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    # Recompute expected hashes
    expected_entries = {}
    valid_blobs = {
        'blob_001.dat': b'BKP1_valid_data_for_file_1',
        'blob_004.dat': b'BKP1_valid_data_for_file_4',
    }

    for filename, content in valid_blobs.items():
        expected_entries[filename] = hashlib.sha256(content).hexdigest()

    with open(manifest_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 entries in manifest, found {len(lines)}"

    parsed_entries = {}
    for line in lines:
        parts = line.split()
        assert len(parts) == 2, f"Invalid line format in manifest: '{line}'"
        parsed_entries[parts[0]] = parts[1]

    for filename, expected_hash in expected_entries.items():
        assert filename in parsed_entries, f"Missing expected file {filename} in manifest"
        assert parsed_entries[filename] == expected_hash, f"Incorrect hash for {filename}. Expected {expected_hash}, got {parsed_entries[filename]}"

def test_no_temp_file_left_behind():
    tmp_path = '/home/user/valid_backups.manifest.tmp'
    assert not os.path.exists(tmp_path), f"Temporary file {tmp_path} should have been renamed or removed"