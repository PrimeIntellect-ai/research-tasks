# test_final_state.py
import os
import hashlib
import tarfile
import pytest

PROJECT_DIR = "/home/user/project"
EXTRACTED_DIR = os.path.join(PROJECT_DIR, "extracted")
MANIFEST_PATH = os.path.join(PROJECT_DIR, "manifest.csv")
RELEASE_PATH = os.path.join(PROJECT_DIR, "release.tar.gz")

EXPECTED_FILES = {
    "config.json": {
        "content": b'{"version":1,"debug":1}',
        "sha256": "3a42c4b82d3ffb4a0db8bd6c813be6cece00435160bb4fdbfb78b88ce8e65df6",
        "size": 22
    },
    "firmware.elf": {
        "content": b'\x7f\x45\x4c\x46\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        "sha256": "24b9148bcf7b2bb2b0bc8c6a01ba262b9a78129e71eab078832a5df09aa1113c",
        "size": 16
    }
}

def test_extracted_directory_exists():
    assert os.path.isdir(EXTRACTED_DIR), f"The directory {EXTRACTED_DIR} does not exist."

def test_extracted_files_content_and_hash():
    for filename, expected in EXPECTED_FILES.items():
        filepath = os.path.join(EXTRACTED_DIR, filename)
        assert os.path.isfile(filepath), f"The file {filepath} does not exist."

        with open(filepath, "rb") as f:
            content = f.read()

        assert len(content) == expected["size"], f"File {filename} size mismatch. Expected {expected['size']}, got {len(content)}."
        assert content == expected["content"], f"File {filename} content mismatch."

        file_hash = hashlib.sha256(content).hexdigest()
        assert file_hash == expected["sha256"], f"File {filename} hash mismatch."

def test_manifest_csv_exists_and_content():
    assert os.path.isfile(MANIFEST_PATH), f"The file {MANIFEST_PATH} does not exist."

    with open(MANIFEST_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected 2 lines in manifest.csv, found {len(lines)}."

    manifest_data = {}
    for line in lines:
        parts = line.split(',')
        assert len(parts) == 2, f"Invalid format in manifest.csv line: '{line}'"
        manifest_data[parts[0]] = parts[1]

    for filename, expected in EXPECTED_FILES.items():
        assert filename in manifest_data, f"{filename} missing from manifest.csv."
        assert manifest_data[filename] == expected["sha256"], f"Hash mismatch in manifest.csv for {filename}."

def test_release_tarball_exists_and_valid():
    assert os.path.isfile(RELEASE_PATH), f"The file {RELEASE_PATH} does not exist."
    assert tarfile.is_tarfile(RELEASE_PATH), f"{RELEASE_PATH} is not a valid tar archive."

    with tarfile.open(RELEASE_PATH, "r:gz") as tar:
        names = tar.getnames()

        # We expect manifest.csv and extracted/ (and its contents)
        manifest_found = any(name.endswith("manifest.csv") for name in names)
        assert manifest_found, "manifest.csv not found in the tarball."

        config_found = any(name.endswith("config.json") for name in names)
        firmware_found = any(name.endswith("firmware.elf") for name in names)

        assert config_found, "config.json not found in the tarball."
        assert firmware_found, "firmware.elf not found in the tarball."