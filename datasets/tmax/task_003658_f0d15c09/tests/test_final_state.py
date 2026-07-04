# test_final_state.py

import os
import json
import hashlib
import pytest

CLEAN_DIR = "/home/user/backups/clean"
MANIFEST_PATH = "/home/user/backups/manifest.json"

EXPECTED_MANIFEST = {
    "recovered_plain.dat": "a251b6819ebf4e1792fc240bd06927d60da11504936d8021307b22591eef350f",
    "recovered_db_dump.txt": "a6fc14daae245d6101ec2926be2a40e1136b6cbdbd5ce4020a67e2315bba98e4",
    "recovered_secret.conf": "43924f793da86c47fc7b8f21915c2cf92bb098a5e1281cb9f257a6e1d2c6c0ca"
}

def compute_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_clean_directory_contents():
    assert os.path.isdir(CLEAN_DIR), f"Directory {CLEAN_DIR} does not exist."

    files = set(os.listdir(CLEAN_DIR))
    expected_files = set(EXPECTED_MANIFEST.keys())

    missing = expected_files - files
    extra = files - expected_files

    assert not missing, f"Missing files in {CLEAN_DIR}: {missing}"
    assert not extra, f"Extra unexpected files in {CLEAN_DIR}: {extra}"

def test_manifest_exists_and_valid():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist."

    try:
        with open(MANIFEST_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Manifest file {MANIFEST_PATH} is not valid JSON.")

    assert isinstance(data, dict), "Manifest JSON should be a dictionary."

def test_manifest_content():
    with open(MANIFEST_PATH, "r") as f:
        data = json.load(f)

    assert data == EXPECTED_MANIFEST, f"Manifest contents do not match expected values.\nExpected: {EXPECTED_MANIFEST}\nGot: {data}"

def test_file_checksums():
    with open(MANIFEST_PATH, "r") as f:
        data = json.load(f)

    for filename, expected_hash in data.items():
        filepath = os.path.join(CLEAN_DIR, filename)
        assert os.path.isfile(filepath), f"File {filepath} listed in manifest does not exist."

        actual_hash = compute_sha256(filepath)
        assert actual_hash == expected_hash, f"Checksum mismatch for {filename}. Expected {expected_hash}, got {actual_hash}."