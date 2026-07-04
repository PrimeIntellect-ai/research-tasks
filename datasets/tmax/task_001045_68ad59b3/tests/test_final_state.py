# test_final_state.py

import os
import json
import hashlib
import pytest

WORKSPACE_DIR = '/home/user/workspace'
EXTRACTED_DIR = os.path.join(WORKSPACE_DIR, 'extracted')
MANIFEST_PATH = os.path.join(WORKSPACE_DIR, 'manifest.json')

def test_zip_slip_prevented():
    """Ensure malicious files were not extracted outside the intended directory."""
    escaped_path = os.path.join(WORKSPACE_DIR, 'escaped.txt')
    absolute_evil_path = '/home/user/absolute_evil.txt'

    assert not os.path.exists(escaped_path), f"Zip slip vulnerability triggered: {escaped_path} exists."
    assert not os.path.exists(absolute_evil_path), f"Zip slip vulnerability triggered: {absolute_evil_path} exists."

def test_extracted_files_exist():
    """Ensure the safe files were properly extracted."""
    assert os.path.isdir(EXTRACTED_DIR), f"Extraction directory {EXTRACTED_DIR} does not exist."

    expected_files = [
        'assets/data1.bin',
        'assets/data2.bin',
        'docs/readme.txt'
    ]

    for rel_path in expected_files:
        full_path = os.path.join(EXTRACTED_DIR, rel_path)
        assert os.path.lexists(full_path), f"Expected file/symlink {rel_path} is missing in {EXTRACTED_DIR}."

def test_deduplication_symlinks():
    """Ensure identical files were deduplicated using relative symlinks."""
    readme_path = os.path.join(EXTRACTED_DIR, 'docs', 'readme.txt')
    data1_path = os.path.join(EXTRACTED_DIR, 'assets', 'data1.bin')

    assert os.path.islink(readme_path), f"Expected {readme_path} to be a symlink."

    target = os.readlink(readme_path)
    assert target == '../assets/data1.bin', f"Symlink target for docs/readme.txt is incorrect. Expected '../assets/data1.bin', got '{target}'."

    assert not os.path.islink(data1_path), f"Expected {data1_path} to be a regular file, not a symlink."

def test_manifest_json_correctness():
    """Ensure the manifest.json is generated correctly according to the spec."""
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist."

    with open(MANIFEST_PATH, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest file {MANIFEST_PATH} is not valid JSON.")

    # Compute expected SHA256 hashes
    def get_sha256(data):
        return hashlib.sha256(data).hexdigest()

    expected_manifest = {
        "assets/data1.bin": {
            "type": "file",
            "sha256": get_sha256(b"Project asset data A"),
            "target": None
        },
        "assets/data2.bin": {
            "type": "file",
            "sha256": get_sha256(b"Project asset data B"),
            "target": None
        },
        "docs/readme.txt": {
            "type": "symlink",
            "sha256": None,
            "target": "../assets/data1.bin"
        }
    }

    assert manifest == expected_manifest, f"Manifest contents do not match expected output.\nExpected: {expected_manifest}\nGot: {manifest}"