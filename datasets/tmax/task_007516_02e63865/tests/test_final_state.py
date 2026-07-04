# test_final_state.py

import os
import json
import hashlib
import pytest

ARTIFACTS_DIR = "/home/user/artifacts"
QUARANTINE_DIR = "/home/user/quarantine"
MANIFEST_PATH = "/home/user/manifest.json"

VALID_FILES = [
    "linux/amd64/app_v1.tar.gz",
    "linux/arm64/app_v1.tar.gz",
    "windows/amd64/app_v2.tar.gz"
]

CORRUPT_FILES = [
    ("linux/amd64/corrupt_app.tar.gz", "corrupt_app.tar.gz"),
    ("windows/amd64/broken_v1.tar.gz", "broken_v1.tar.gz")
]

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_manifest_exists_and_format():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file not found at {MANIFEST_PATH}"

    with open(MANIFEST_PATH, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not a valid JSON file")

    assert "files" in manifest, "Manifest JSON missing 'files' key"
    assert isinstance(manifest["files"], list), "'files' in manifest is not a list"

def test_manifest_contents():
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    actual_files = manifest["files"]

    # Check sorting
    paths = [item.get("path") for item in actual_files]
    assert paths == sorted(paths), "The 'files' array in manifest.json is not sorted alphabetically by 'path'"

    expected_files = []
    for rel_path in VALID_FILES:
        full_path = os.path.join(ARTIFACTS_DIR, rel_path)
        assert os.path.isfile(full_path), f"Valid artifact {full_path} should still exist"
        checksum = get_sha256(full_path)
        expected_files.append({
            "path": rel_path,
            "checksum": checksum
        })

    expected_files.sort(key=lambda x: x["path"])

    assert actual_files == expected_files, "Manifest contents do not match the expected valid files and their checksums"

def test_quarantine_directory():
    assert os.path.isdir(QUARANTINE_DIR), f"Quarantine directory missing at {QUARANTINE_DIR}"

    quarantined_files = os.listdir(QUARANTINE_DIR)
    expected_quarantined = [name for _, name in CORRUPT_FILES]

    assert sorted(quarantined_files) == sorted(expected_quarantined), \
        f"Quarantine directory should contain exactly {expected_quarantined}, but found {quarantined_files}"

def test_corrupt_files_removed_from_artifacts():
    for rel_path, _ in CORRUPT_FILES:
        full_path = os.path.join(ARTIFACTS_DIR, rel_path)
        assert not os.path.exists(full_path), f"Corrupted file {full_path} was not removed from the artifacts directory"