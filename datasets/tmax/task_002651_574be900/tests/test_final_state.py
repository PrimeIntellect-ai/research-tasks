# test_final_state.py

import os
import hashlib
import tarfile
import pytest

CONFIGS_DIR = "/home/user/configs"
NEW_MANIFEST = "/home/user/new_manifest.txt"
CONFIG_PATCH_TAR = "/home/user/config_patch.tar"
BASE_MANIFEST = "/home/user/base_manifest.txt"

def compute_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def test_new_manifest_correctness():
    assert os.path.isfile(NEW_MANIFEST), f"New manifest not found at {NEW_MANIFEST}"

    # Compute expected manifest
    expected_lines = []
    for filename in os.listdir(CONFIGS_DIR):
        filepath = os.path.join(CONFIGS_DIR, filename)
        if os.path.isfile(filepath):
            file_hash = compute_sha256(filepath)
            expected_lines.append(f"{file_hash} {filename}")

    expected_lines.sort()
    expected_content = "\n".join(expected_lines) + "\n"

    with open(NEW_MANIFEST, 'r') as f:
        actual_content = f.read()

    # Standardize line endings just in case
    actual_lines = [line.strip() for line in actual_content.strip().split('\n') if line.strip()]
    expected_lines_clean = [line.strip() for line in expected_content.strip().split('\n') if line.strip()]

    assert actual_lines == expected_lines_clean, f"Manifest contents are incorrect. Expected:\n{expected_lines_clean}\nGot:\n{actual_lines}"

def test_config_patch_tar_contents():
    assert os.path.isfile(CONFIG_PATCH_TAR), f"Tar archive not found at {CONFIG_PATCH_TAR}"

    # Determine which files should be in the tar archive
    # Read base manifest
    base_hashes = {}
    if os.path.isfile(BASE_MANIFEST):
        with open(BASE_MANIFEST, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    base_hashes[parts[1]] = parts[0]

    expected_files_in_tar = set()
    for filename in os.listdir(CONFIGS_DIR):
        filepath = os.path.join(CONFIGS_DIR, filename)
        if os.path.isfile(filepath):
            current_hash = compute_sha256(filepath)
            if filename not in base_hashes or base_hashes[filename] != current_hash:
                expected_files_in_tar.add(filename)

    # Read tar archive
    try:
        with tarfile.open(CONFIG_PATCH_TAR, "r") as tar:
            tar_members = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"Could not read {CONFIG_PATCH_TAR} as a valid tar archive.")

    # Check that paths are relative (just the filename)
    actual_files_in_tar = set()
    for member in tar_members:
        # Reject absolute paths or paths containing directories
        assert "/" not in member and "\\" not in member, f"Tar archive contains directory paths or absolute paths: {member}. Expected just filenames."
        actual_files_in_tar.add(member)

    assert actual_files_in_tar == expected_files_in_tar, f"Tar archive contents mismatch. Expected {expected_files_in_tar}, got {actual_files_in_tar}"