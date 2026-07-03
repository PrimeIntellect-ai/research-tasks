# test_final_state.py

import os
import json
import hashlib
import re
import pytest

ARCHIVE_DIR = "/home/user/archive"
MANIFEST_PATH = os.path.join(ARCHIVE_DIR, "manifest.json")

def get_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def test_manifest_exists():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"

def test_manifest_contents_and_chunks():
    with open(MANIFEST_PATH, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not valid JSON")

    assert isinstance(manifest, dict), "Manifest must be a JSON object (dictionary)"
    assert len(manifest) > 0, "Manifest is empty"

    chunk_files = sorted([f for f in os.listdir(ARCHIVE_DIR) if f.startswith("chunk_") and f.endswith(".txt")])
    assert len(chunk_files) > 0, "No chunk files found in archive directory"

    # Check that manifest keys match chunk files exactly
    assert set(manifest.keys()) == set(chunk_files), "Manifest keys do not match the chunk files present"

    # Verify checksums
    for chunk_file, expected_hash in manifest.items():
        chunk_path = os.path.join(ARCHIVE_DIR, chunk_file)
        actual_hash = get_sha256(chunk_path)
        assert actual_hash == expected_hash, f"Checksum mismatch for {chunk_file}. Expected {expected_hash}, got {actual_hash}"

def test_chunk_contents():
    chunk_files = sorted([f for f in os.listdir(ARCHIVE_DIR) if f.startswith("chunk_") and f.endswith(".txt")])

    ipv4_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    for i, chunk_file in enumerate(chunk_files):
        chunk_path = os.path.join(ARCHIVE_DIR, chunk_file)
        with open(chunk_path, 'r') as f:
            lines = f.readlines()

        # All but the last chunk should have exactly 50 lines
        if i < len(chunk_files) - 1:
            assert len(lines) == 50, f"{chunk_file} does not have exactly 50 lines"
        else:
            assert len(lines) <= 50, f"{chunk_file} has more than 50 lines"
            assert len(lines) > 0, f"{chunk_file} is empty"

        for line_num, line in enumerate(lines, 1):
            assert "DEBUG" not in line, f"Found 'DEBUG' in {chunk_file} at line {line_num}"
            assert not ipv4_pattern.search(line), f"Found unmasked IPv4 address in {chunk_file} at line {line_num}"