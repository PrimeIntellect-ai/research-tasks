# test_final_state.py

import os
import hashlib
import tarfile
import pytest

APP_DATA_DIR = "/home/user/app_data"
MANIFEST_PATH = "/home/user/manifest.txt"
TAR_PATH = "/home/user/clean_logs.tar"

def get_expected_log_files():
    # These are the regular .log files created in the setup
    return [
        f"{APP_DATA_DIR}/module_a/access.log",
        f"{APP_DATA_DIR}/module_a/error.log",
        f"{APP_DATA_DIR}/module_b/nested/deep.log",
        f"{APP_DATA_DIR}/module_b/system.log",
    ]

def compute_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_manifest_exists_and_correct():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist or is not a regular file."

    expected_files = sorted(get_expected_log_files())
    expected_lines = []
    for f in expected_files:
        assert os.path.isfile(f), f"Expected log file {f} is missing from the filesystem."
        h = compute_sha256(f)
        expected_lines.append(f"{h} {f}\n")

    with open(MANIFEST_PATH, "r") as f:
        actual_lines = f.readlines()

    assert len(actual_lines) == len(expected_lines), f"Manifest has {len(actual_lines)} lines, expected {len(expected_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Manifest line {i+1} mismatch. Expected: {expected.strip()}, Actual: {actual.strip()}"

def test_tar_archive_exists_and_correct():
    assert os.path.isfile(TAR_PATH), f"Tar archive {TAR_PATH} does not exist or is not a regular file."

    expected_files = sorted(get_expected_log_files())

    try:
        with tarfile.open(TAR_PATH, "r") as tar:
            tar_members = tar.getnames()
    except tarfile.TarError as e:
        pytest.fail(f"Failed to read tar archive {TAR_PATH}: {e}")

    actual_files = sorted(tar_members)

    assert actual_files == expected_files, f"Tar archive contents mismatch.\nExpected: {expected_files}\nActual: {actual_files}"