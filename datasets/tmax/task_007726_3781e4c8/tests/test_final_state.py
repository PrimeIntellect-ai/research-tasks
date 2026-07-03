# test_final_state.py

import os
import hashlib
import tarfile
import pytest

ARTIFACTS_DIR = "/home/user/artifacts"
CHECKSUMS_FILE = "/home/user/checksums.txt"
RELEASE_ARCHIVE = "/home/user/release.tar.gz"

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def test_deduplicate_binaries():
    # Check that duplicates were removed and the alphabetically first one was kept
    assert not os.path.exists(os.path.join(ARTIFACTS_DIR, "m_dup.bin")), "m_dup.bin should have been deleted"
    assert not os.path.exists(os.path.join(ARTIFACTS_DIR, "z_dup.bin")), "z_dup.bin should have been deleted"

    assert os.path.exists(os.path.join(ARTIFACTS_DIR, "a_dup.bin")), "a_dup.bin should have been kept"
    assert os.path.exists(os.path.join(ARTIFACTS_DIR, "unique.bin")), "unique.bin should have been kept"

def test_fix_text_configurations():
    # Check that active text files were updated
    t1_path = os.path.join(ARTIFACTS_DIR, "t1.txt")
    assert os.path.exists(t1_path), "t1.txt is missing"
    with open(t1_path, 'r') as f:
        content = f.read()
    assert "PROD_SERVER" in content, "t1.txt should have DEV_SERVER replaced with PROD_SERVER"
    assert "DEV_SERVER" not in content, "t1.txt should not contain DEV_SERVER anymore"

    # Check that archived text files were NOT updated
    t3_path = os.path.join(ARTIFACTS_DIR, "t3_archived.txt")
    assert os.path.exists(t3_path), "t3_archived.txt is missing"
    with open(t3_path, 'r') as f:
        content = f.read()
    assert "DEV_SERVER" in content, "t3_archived.txt should still contain DEV_SERVER"
    assert "PROD_SERVER" not in content, "t3_archived.txt should not have been updated"

def test_generate_manifest():
    assert os.path.exists(CHECKSUMS_FILE), f"Manifest file {CHECKSUMS_FILE} does not exist"

    expected_files = ["a_dup.bin", "t1.txt", "t2.txt", "t3_archived.txt", "unique.bin"]
    expected_lines = []

    for fname in expected_files:
        fpath = os.path.join(ARTIFACTS_DIR, fname)
        if os.path.exists(fpath):
            expected_lines.append(f"{get_file_hash(fpath)}  {fname}")

    # Read the actual checksums file
    with open(CHECKSUMS_FILE, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    # Standardize spaces for comparison (some sha256sum versions use two spaces, some use one space + asterisk)
    actual_parsed = []
    for line in actual_lines:
        parts = line.split()
        if len(parts) >= 2:
            # handle cases where there might be an asterisk or path prefix
            h = parts[0]
            name = parts[-1].split('/')[-1]
            actual_parsed.append(f"{h}  {name}")

    actual_parsed.sort()
    expected_lines.sort()

    assert actual_parsed == expected_lines, "Checksums manifest does not match the expected output for remaining files"

def test_package_release():
    assert os.path.exists(RELEASE_ARCHIVE), f"Release archive {RELEASE_ARCHIVE} does not exist"
    assert tarfile.is_tarfile(RELEASE_ARCHIVE), f"{RELEASE_ARCHIVE} is not a valid tar archive"

    expected_active_files = {"a_dup.bin", "unique.bin", "t1.txt", "t2.txt"}
    unexpected_files = {"m_dup.bin", "z_dup.bin", "t3_archived.txt", "inventory.txt"}

    with tarfile.open(RELEASE_ARCHIVE, 'r:gz') as tar:
        members = tar.getnames()

    # Extract basenames to handle potential directory structures inside tar
    basenames = {os.path.basename(m) for m in members if not m.endswith('/') and os.path.basename(m)}

    for f in expected_active_files:
        assert f in basenames, f"Expected active file {f} is missing from the release archive"

    for f in unexpected_files:
        assert f not in basenames, f"File {f} should NOT be in the release archive"