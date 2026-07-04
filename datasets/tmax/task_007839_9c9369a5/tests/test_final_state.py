# test_final_state.py

import os
import json
import tarfile
import hashlib
import pytest

EXTRACTED_DIR = "/home/user/extracted"
NEW_MANIFEST = "/home/user/new_manifest.json"
BACKUP_ARCHIVE = "/home/user/incremental_backup.tar.gz"

def test_zip_slip_prevented():
    # Check that files with malicious paths were not extracted outside the target dir
    assert not os.path.exists("/home/user/evil.sh"), "Zip slip vulnerability allowed extraction of evil.sh to /home/user/"
    assert not os.path.exists("/absolute/evil.txt"), "Zip slip vulnerability allowed extraction of absolute/evil.txt"

    # Also check they are not somehow inside the extracted dir with weird names
    assert not os.path.exists(os.path.join(EXTRACTED_DIR, "evil.sh")), "evil.sh should have been ignored"
    assert not os.path.exists(os.path.join(EXTRACTED_DIR, "absolute", "evil.txt")), "evil.txt should have been ignored"

def test_extracted_and_converted_files():
    # Expected files and their contents
    expected_files = {
        "valid1.bin": b"Hello",
        "valid2.txt": b"World",
        "subdir/valid3.bin": b"Go",
        "subdir2/valid4.txt": b"NewFile"
    }

    for rel_path, expected_content in expected_files.items():
        abs_path = os.path.join(EXTRACTED_DIR, rel_path)
        assert os.path.isfile(abs_path), f"Expected file {abs_path} does not exist"
        with open(abs_path, "rb") as f:
            content = f.read()
        assert content == expected_content, f"Content of {abs_path} is incorrect. Expected {expected_content}, got {content}"

def test_hex_files_deleted():
    assert not os.path.exists(os.path.join(EXTRACTED_DIR, "valid1.hex")), "valid1.hex was not deleted after conversion"
    assert not os.path.exists(os.path.join(EXTRACTED_DIR, "subdir", "valid3.hex")), "subdir/valid3.hex was not deleted after conversion"

def test_new_manifest_generation():
    assert os.path.isfile(NEW_MANIFEST), f"Manifest file {NEW_MANIFEST} does not exist"

    with open(NEW_MANIFEST, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{NEW_MANIFEST} is not valid JSON")

    expected_hashes = {
        "valid1.bin": hashlib.sha256(b"Hello").hexdigest(),
        "valid2.txt": hashlib.sha256(b"World").hexdigest(),
        "subdir/valid3.bin": hashlib.sha256(b"Go").hexdigest(),
        "subdir2/valid4.txt": hashlib.sha256(b"NewFile").hexdigest()
    }

    for rel_path, expected_hash in expected_hashes.items():
        assert rel_path in manifest, f"{rel_path} is missing from the new manifest"
        assert manifest[rel_path] == expected_hash, f"Hash for {rel_path} is incorrect in the manifest"

    # Ensure no extra files in manifest
    for rel_path in manifest.keys():
        assert rel_path in expected_hashes, f"Unexpected file {rel_path} found in manifest"

def test_incremental_backup_archive():
    assert os.path.isfile(BACKUP_ARCHIVE), f"Backup archive {BACKUP_ARCHIVE} does not exist"
    assert tarfile.is_tarfile(BACKUP_ARCHIVE), f"{BACKUP_ARCHIVE} is not a valid tar archive"

    with tarfile.open(BACKUP_ARCHIVE, "r:gz") as tar:
        members = tar.getnames()

        # Normalize paths to avoid issues with leading './' or similar
        normalized_members = [os.path.normpath(m) for m in members]

        # Files that should be in the backup
        expected_in_backup = ["subdir/valid3.bin", "subdir2/valid4.txt"]
        for expected in expected_in_backup:
            # Check if the expected file path is in the normalized members
            # Allow for paths to be prefixed with './' or similar by doing a suffix match
            found = any(m == expected or m.endswith('/' + expected) for m in normalized_members)
            assert found, f"{expected} is missing from the incremental backup"

        # Files that should NOT be in the backup
        not_expected_in_backup = ["valid1.bin", "valid2.txt"]
        for not_expected in not_expected_in_backup:
            found = any(m == not_expected or m.endswith('/' + not_expected) for m in normalized_members)
            assert not found, f"{not_expected} should not be in the incremental backup"