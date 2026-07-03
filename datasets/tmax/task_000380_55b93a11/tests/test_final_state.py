# test_final_state.py

import os
import json
import hashlib
import pytest

MANIFEST_PATH = "/home/user/organized_files/manifest.json"
TMP_MANIFEST_PATH = "/home/user/organized_files/manifest.json.tmp"

EXPECTED_FILES = {
    "elf": [
        "/home/user/project_files/builds/v1/firmware_v1.bin",
        "/home/user/project_files/builds/v2/fw_v2_final.out"
    ],
    "gcode": [
        "/home/user/project_files/models/bracket.gcode",
        "/home/user/project_files/models/gear.gcode"
    ]
}

def compute_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def test_manifest_exists_and_tmp_does_not():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"
    assert not os.path.exists(TMP_MANIFEST_PATH), f"Temporary manifest file {TMP_MANIFEST_PATH} should have been renamed or removed."

def test_manifest_content_and_symlinks():
    assert os.path.isfile(MANIFEST_PATH), "Manifest file missing"

    with open(MANIFEST_PATH, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not valid JSON")

    assert isinstance(manifest, dict), "Manifest should be a JSON dictionary"

    # Compute expected manifest entries
    expected_manifest = {}
    for category, paths in EXPECTED_FILES.items():
        for path in paths:
            assert os.path.isfile(path), f"Original file missing: {path}"
            checksum = compute_sha256(path)
            prefix = checksum[:8]
            filename = os.path.basename(path)
            symlink_name = f"{filename}_{prefix}"
            symlink_path = f"/home/user/organized_files/{category}/{symlink_name}"

            expected_manifest[symlink_path] = {
                "original_path": path,
                "checksum": checksum
            }

    # Verify manifest keys match exactly
    assert set(manifest.keys()) == set(expected_manifest.keys()), \
        f"Manifest keys do not match expected symlink paths. Expected: {list(expected_manifest.keys())}, Got: {list(manifest.keys())}"

    # Verify each entry and the actual symlinks
    for symlink_path, expected_data in expected_manifest.items():
        actual_data = manifest[symlink_path]

        assert actual_data.get("original_path") == expected_data["original_path"], \
            f"Incorrect original_path in manifest for {symlink_path}"
        assert actual_data.get("checksum") == expected_data["checksum"], \
            f"Incorrect checksum in manifest for {symlink_path}"

        # Check that the symlink actually exists
        assert os.path.islink(symlink_path), f"Expected a symbolic link at {symlink_path}"

        # Check that the symlink points to the correct original file
        target = os.readlink(symlink_path)
        assert target == expected_data["original_path"], \
            f"Symlink {symlink_path} points to {target}, expected {expected_data['original_path']}"