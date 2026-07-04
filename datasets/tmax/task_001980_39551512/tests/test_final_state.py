# test_final_state.py

import os
import hashlib
import struct
import pytest

def test_extract_metadata_c_exists_and_uses_mmap():
    c_file = '/home/user/extract_metadata.c'
    assert os.path.exists(c_file), f"File {c_file} is missing."
    with open(c_file, 'r') as f:
        content = f.read()
    assert 'mmap' in content, f"The C program {c_file} must use 'mmap'."

def test_raw_metadata_txt():
    raw_file = '/home/user/raw_metadata.txt'
    assert os.path.exists(raw_file), f"File {raw_file} is missing."

    expected_lines = [
        "ID:1001|DATE:20231015|STATUS:A",
        "ID:1002|DATE:20231016|STATUS:B",
        "ID:1003|DATE:20231017|STATUS:C"
    ]

    with open(raw_file, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, f"Content of {raw_file} is incorrect. Expected {expected_lines}, got {actual_lines}."

def test_clean_metadata_csv():
    csv_file = '/home/user/clean_metadata.csv'
    assert os.path.exists(csv_file), f"File {csv_file} is missing."

    expected_lines = [
        "1001,20231015,A",
        "1002,20231016,B",
        "1003,20231017,C"
    ]

    with open(csv_file, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, f"Content of {csv_file} is incorrect. Expected {expected_lines}, got {actual_lines}."

def test_manifest_txt():
    csv_file = '/home/user/clean_metadata.csv'
    manifest_file = '/home/user/manifest.txt'

    assert os.path.exists(csv_file), f"File {csv_file} is missing, cannot verify manifest."
    assert os.path.exists(manifest_file), f"File {manifest_file} is missing."

    # Compute the actual SHA-256 hash of the generated clean_metadata.csv
    hasher = hashlib.sha256()
    with open(csv_file, 'rb') as f:
        hasher.update(f.read())
    expected_hash = hasher.hexdigest()

    with open(manifest_file, 'r') as f:
        manifest_content = f.read().strip()

    # The output format should exactly match standard `sha256sum`, e.g., `<hash>  clean_metadata.csv`
    # However, we'll just check if the hash is present and the filename is correct to be robust against minor spacing differences
    assert expected_hash in manifest_content, f"Manifest {manifest_file} does not contain the correct hash {expected_hash} for {csv_file}."
    assert "clean_metadata.csv" in manifest_content, f"Manifest {manifest_file} does not contain the filename 'clean_metadata.csv'."

    # Check exact format if possible
    expected_manifest_line = f"{expected_hash}  clean_metadata.csv"
    assert manifest_content == expected_manifest_line or manifest_content == f"{expected_hash} *clean_metadata.csv", \
        f"Manifest format is incorrect. Expected '{expected_manifest_line}', got '{manifest_content}'."