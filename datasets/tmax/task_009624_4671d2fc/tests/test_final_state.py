# test_final_state.py

import os
import csv
import hashlib
import pytest

MANIFEST_PATH = "/home/user/manifest.csv"
EXTRACTED_DIR = "/home/user/repository_extracted"

EXPECTED_HASHES = {
    "076ebdd2652db7e1bb7270fc6cf16fb13c9df920f7797cf43b9e4a3bfec8f438", # client
    "b109e51c86d8cb27dfd8a86a6abcfca2ca1f0bf1ec7eddf95c47fb5af82622df", # server
    "1bc832eddd683c3189912be21dc91f543e5904de970f5e1f0e42d76378e1c6b8", # libcore
    "3f48682cdb66bd1095bf8107ef4f0ebf0f970ea4541bf777e434f82635a82208", # libnet
}

def test_manifest_exists():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"
    assert os.path.isfile(MANIFEST_PATH), f"Path {MANIFEST_PATH} is not a file"

def test_manifest_content_and_sorting():
    assert os.path.exists(MANIFEST_PATH), "Manifest file missing"

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 entries in manifest, found {len(lines)}"

    paths = []
    hashes = set()

    for line in lines:
        parts = line.split(",")
        assert len(parts) == 2, f"Invalid manifest line format: {line}"
        path, sha256_hash = parts
        paths.append(path)
        hashes.add(sha256_hash.lower())

        # Check if the file actually exists at the stated relative path
        abs_path = os.path.join(EXTRACTED_DIR, path)
        assert os.path.exists(abs_path), f"File {path} listed in manifest does not exist in {EXTRACTED_DIR}"

        # Verify it's an ELF file
        with open(abs_path, "rb") as bf:
            header = bf.read(4)
            assert header == b"\x7fELF", f"File {path} is not an ELF binary"

        # Verify the hash matches the actual file
        with open(abs_path, "rb") as bf:
            file_hash = hashlib.sha256(bf.read()).hexdigest()
            assert file_hash == sha256_hash.lower(), f"Hash mismatch for {path}: expected {file_hash}, got {sha256_hash}"

    assert hashes == EXPECTED_HASHES, f"Hashes in manifest do not match expected ELF hashes. Got {hashes}"

    # Check alphabetical sorting by relative_path
    sorted_paths = sorted(paths)
    assert paths == sorted_paths, "Manifest entries are not sorted alphabetically by relative_path"

def test_no_archives_remain():
    assert os.path.exists(EXTRACTED_DIR), f"Extracted directory missing at {EXTRACTED_DIR}"

    archive_extensions = ('.zip', '.tar.gz', '.tar.bz2', '.tgz', '.tbz2', '.tar')

    for root, dirs, files in os.walk(EXTRACTED_DIR):
        for file in files:
            assert not file.endswith(archive_extensions), f"Archive file {file} was not deleted from {root}"