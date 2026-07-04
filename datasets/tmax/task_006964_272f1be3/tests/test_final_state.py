# test_final_state.py

import os
import json
import hashlib
import tarfile
import pytest

MANIFEST_PATH = "/home/user/backup_manifest.json"
ARCHIVE_PATH = "/home/user/project_backup.tar.gz"
PROJECT_DATA_DIR = "/home/user/project_data"

def compute_sha256(file_path):
    """Compute the SHA-256 checksum of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def test_manifest_exists_and_valid_json():
    """Check if the manifest file exists and is valid JSON."""
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"
    try:
        with open(MANIFEST_PATH, 'r') as f:
            manifest = json.load(f)
    except json.JSONDecodeError:
        pytest.fail("Manifest file is not valid JSON.")

    assert "files" in manifest, "Manifest is missing the 'files' key."
    assert "circular_links" in manifest, "Manifest is missing the 'circular_links' key."

def test_manifest_files_content():
    """Verify the 'files' dictionary in the manifest."""
    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)

    files_dict = manifest.get("files", {})

    expected_files = [
        "src/hello.txt",
        "src/config.txt",
        "assets/blob.bin"
    ]

    # Check that all expected files are in the manifest
    for rel_path in expected_files:
        assert rel_path in files_dict, f"Expected file {rel_path} missing from manifest 'files'."

        # Verify checksum
        abs_path = os.path.join(PROJECT_DATA_DIR, rel_path)
        expected_checksum = compute_sha256(abs_path)
        assert files_dict[rel_path] == expected_checksum, f"Checksum mismatch for {rel_path}."

    # Ensure no extra files are included
    assert len(files_dict) == len(expected_files), f"Manifest 'files' contains extra entries: {set(files_dict.keys()) - set(expected_files)}"

def test_manifest_circular_links_content():
    """Verify the 'circular_links' list in the manifest."""
    with open(MANIFEST_PATH, 'r') as f:
        manifest = json.load(f)

    circular_links = manifest.get("circular_links", [])

    expected_links = [
        "links/loop_a",
        "links/loop_b",
        "links/loop_c",
        "links/self_loop"
    ]

    # Check exact match and sorting
    assert isinstance(circular_links, list), "'circular_links' must be a list."
    assert sorted(circular_links) == circular_links, "'circular_links' must be sorted."
    assert set(circular_links) == set(expected_links), f"Expected circular links {expected_links}, got {circular_links}."

def test_archive_exists_and_valid():
    """Check if the archive exists and is a valid tar.gz file."""
    assert os.path.isfile(ARCHIVE_PATH), f"Archive file missing at {ARCHIVE_PATH}"
    assert tarfile.is_tarfile(ARCHIVE_PATH), "Archive is not a valid tar file."

def test_archive_contents():
    """Verify the contents of the tar archive."""
    expected_files = {
        "src/hello.txt",
        "src/config.txt",
        "assets/blob.bin"
    }

    actual_files = set()
    with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
        for member in tar.getmembers():
            # Ensure no directories or symlinks are included as empty entries
            assert member.isfile(), f"Archive contains non-regular file entry: {member.name}"
            actual_files.add(member.name)

    assert actual_files == expected_files, f"Archive contents mismatch. Expected {expected_files}, got {actual_files}."