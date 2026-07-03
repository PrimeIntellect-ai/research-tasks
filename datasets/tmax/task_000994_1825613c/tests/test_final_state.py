# test_final_state.py

import os
import tarfile
import hashlib
import pytest

CURATED_DIR = "/home/user/curated"
MANIFEST_PATH = "/home/user/manifest.txt"
TARBALL_PATH = "/home/user/curated_artifacts.tar.gz"

EXPECTED_FILES = {
    "core_engine.bin",
    "libhelper.so",
    "plugin.bin",
    "libnet.so"
}

def test_curated_directory_contents():
    """Test that the curated directory contains exactly the expected valid binary artifacts."""
    assert os.path.isdir(CURATED_DIR), f"Directory {CURATED_DIR} does not exist."
    files = set(os.listdir(CURATED_DIR))
    assert files == EXPECTED_FILES, f"Expected files in {CURATED_DIR} to be {EXPECTED_FILES}, but got {files}."

def test_manifest_file():
    """Test that the manifest file exists and contains the correct SHA256 checksums."""
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist."

    # Compute expected manifest
    expected_lines = []
    for filename in sorted(EXPECTED_FILES):
        filepath = os.path.join(CURATED_DIR, filename)
        assert os.path.isfile(filepath), f"File {filepath} is missing, cannot compute checksum."
        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        expected_lines.append(f"{file_hash}  {filename}")

    expected_manifest = "\n".join(expected_lines)

    with open(MANIFEST_PATH, "r") as f:
        actual_manifest = f.read().strip()

    assert actual_manifest == expected_manifest, "Manifest contents do not match expected output (sorted by filename, with correct format)."

def test_curated_artifacts_tarball():
    """Test that the final tarball exists, is gzip-compressed, and contains the curated artifacts."""
    assert os.path.isfile(TARBALL_PATH), f"Tarball {TARBALL_PATH} does not exist."
    assert tarfile.is_tarfile(TARBALL_PATH), f"File {TARBALL_PATH} is not a valid tar archive."

    try:
        with tarfile.open(TARBALL_PATH, "r:gz") as tar:
            names = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"Tarball {TARBALL_PATH} could not be read as a gzip-compressed tar archive.")

    expected_tar_files = {f"curated/{f}" for f in EXPECTED_FILES}

    # Normalize paths by stripping leading './' just in case
    actual_files = {name.lstrip("./") for name in names}

    for ef in expected_tar_files:
        assert ef in actual_files, f"Expected file {ef} missing from tarball {TARBALL_PATH}."