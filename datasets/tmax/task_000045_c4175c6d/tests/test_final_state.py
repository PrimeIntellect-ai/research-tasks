# test_final_state.py

import os
import json
import hashlib
import pytest

def test_manifest_exists_and_valid_json():
    manifest_path = '/home/user/backup_manifest.json'
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing. The Go program must generate this file."

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest file {manifest_path} is not valid JSON.")

    assert "files" in manifest, "Manifest JSON must contain a 'files' key at the root level."
    assert isinstance(manifest["files"], list), "The 'files' key in the manifest must be a list."

def test_manifest_content_and_checksums():
    manifest_path = '/home/user/backup_manifest.json'
    if not os.path.isfile(manifest_path):
        pytest.skip("Manifest file missing, skipping content test.")

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Manifest is not valid JSON, skipping content test.")

    # We dynamically compute the expected state based on the actual valid files in the environment
    expected_files = []
    known_valid_paths = [
        '/home/user/backup_source/level1/level2/valid2.bin',
        '/home/user/backup_source/valid1.bin'
    ]

    for path in known_valid_paths:
        assert os.path.isfile(path), f"Expected valid backup file {path} is missing from the system."
        with open(path, 'rb') as f:
            content = f.read()
            # Verify the file actually has the correct magic bytes before adding to expected
            assert content.startswith(b"BKP\x01"), f"File {path} does not have the correct magic bytes."
            checksum = hashlib.sha256(content).hexdigest()
            expected_files.append({
                "path": path,
                "checksum": checksum
            })

    # The output must be sorted alphabetically by path
    expected_files.sort(key=lambda x: x["path"])

    actual_files = manifest.get("files", [])

    assert len(actual_files) == len(expected_files), (
        f"Expected {len(expected_files)} valid files in the manifest, but found {len(actual_files)}. "
        "Ensure invalid files and symlink loops are properly ignored."
    )

    for i, (expected, actual) in enumerate(zip(expected_files, actual_files)):
        assert actual.get("path") == expected["path"], (
            f"File path mismatch at index {i}. Expected '{expected['path']}', got '{actual.get('path')}'. "
            "Ensure paths are absolute and sorted alphabetically."
        )
        assert actual.get("checksum") == expected["checksum"], (
            f"Checksum mismatch for {expected['path']}. Expected '{expected['checksum']}', got '{actual.get('checksum')}'."
        )