# test_final_state.py

import os
import hashlib
import tarfile
import pytest

RAW_DATA_DIR = "/home/user/raw_data"
MANIFEST_PATH = "/home/user/checksums.sha256"
TARBALL_PATH = "/home/user/secure_backup.tar.gz"

EXPECTED_FILES = {
    "project-alpha.doc": b"project info",
    "financial-report-2023.xls": b"money",
    "image-001.jpg": b"fake image",
    "notes.txt": b"just notes",
}

def test_renamed_files_and_content():
    assert os.path.isdir(RAW_DATA_DIR), f"Directory {RAW_DATA_DIR} does not exist."

    actual_files = set(os.listdir(RAW_DATA_DIR))
    expected_filenames = set(EXPECTED_FILES.keys())

    missing_files = expected_filenames - actual_files
    extra_files = actual_files - expected_filenames

    assert not missing_files, f"Missing renamed files in {RAW_DATA_DIR}: {missing_files}"
    assert not extra_files, f"Unexpected or unrenamed files in {RAW_DATA_DIR}: {extra_files}"

    for filename, expected_content in EXPECTED_FILES.items():
        filepath = os.path.join(RAW_DATA_DIR, filename)
        with open(filepath, "rb") as f:
            content = f.read()
        assert content == expected_content, f"Content of {filename} is incorrect."

def test_checksum_manifest():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist."

    # Compute expected hashes
    expected_lines = []
    for filename, content in EXPECTED_FILES.items():
        file_hash = hashlib.sha256(content).hexdigest()
        expected_lines.append(f"{file_hash}  {filename}")

    with open(MANIFEST_PATH, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), "Manifest does not contain the correct number of entries."

    for expected_line in expected_lines:
        assert expected_line in actual_lines, f"Expected entry '{expected_line}' not found in manifest."

def test_tarball_exists_and_contents():
    assert os.path.isfile(TARBALL_PATH), f"Tarball {TARBALL_PATH} does not exist."
    assert tarfile.is_tarfile(TARBALL_PATH), f"{TARBALL_PATH} is not a valid tar archive."

    with tarfile.open(TARBALL_PATH, "r:gz") as tar:
        members = tar.getnames()

    # Normalize paths to check if they match expected structure
    # They should be either exactly "raw_data/...", "./raw_data/...", "checksums.sha256", "./checksums.sha256"
    normalized_members = set()
    for m in members:
        # Remove leading './' if present
        if m.startswith("./"):
            m = m[2:]
        normalized_members.add(m)

    expected_members = {"checksums.sha256", "raw_data"}
    for filename in EXPECTED_FILES.keys():
        expected_members.add(f"raw_data/{filename}")

    # The tarball might not explicitly contain the directory entry 'raw_data', but it must contain the files
    for filename in EXPECTED_FILES.keys():
        assert f"raw_data/{filename}" in normalized_members, f"Tarball is missing raw_data/{filename}"

    assert "checksums.sha256" in normalized_members, "Tarball is missing checksums.sha256"