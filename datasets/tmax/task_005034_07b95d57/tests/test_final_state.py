# test_final_state.py

import os
import json
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace"
BUILDER_DIR = os.path.join(WORKSPACE_DIR, "builder")
BUILD_DIR = os.path.join(BUILDER_DIR, "build")
PACKAGER_BIN = os.path.join(BUILD_DIR, "packager")
LIB_ARCHIVER = os.path.join(BUILD_DIR, "libarchiver.so")
MANIFEST_PY = os.path.join(WORKSPACE_DIR, "manifest.py")
FINAL_MANIFEST = os.path.join(WORKSPACE_DIR, "final_manifest.json")

def compute_expected_checksum(filepath):
    full_path = os.path.join(WORKSPACE_DIR, filepath)
    if not os.path.isfile(full_path):
        return None
    with open(full_path, "rb") as f:
        data = f.read()
    checksum = 0
    for byte in data:
        checksum ^= byte
    return f"{checksum:02x}"

def test_build_artifacts_exist():
    assert os.path.isfile(PACKAGER_BIN), f"Expected executable not found: {PACKAGER_BIN}"
    assert os.access(PACKAGER_BIN, os.X_OK), f"File is not executable: {PACKAGER_BIN}"
    assert os.path.isfile(LIB_ARCHIVER), f"Expected shared library not found: {LIB_ARCHIVER}"

def test_packager_runs_without_ld_library_path():
    # Run the packager binary without LD_LIBRARY_PATH to verify RPATH is set correctly
    env = os.environ.copy()
    if "LD_LIBRARY_PATH" in env:
        del env["LD_LIBRARY_PATH"]

    test_file = os.path.join(BUILDER_DIR, "src", "packager.c")
    try:
        result = subprocess.run([PACKAGER_BIN, test_file], env=env, capture_output=True, text=True, cwd=BUILD_DIR)
        assert result.returncode == 0, f"packager failed to run. Output: {result.stderr}"
        assert len(result.stdout.strip()) == 2, f"Unexpected output from packager: {result.stdout}"
    except Exception as e:
        pytest.fail(f"Failed to execute packager: {e}")

def test_manifest_py_exists():
    assert os.path.isfile(MANIFEST_PY), f"Python script not found: {MANIFEST_PY}"

def test_final_manifest_json():
    assert os.path.isfile(FINAL_MANIFEST), f"Final manifest not found: {FINAL_MANIFEST}"

    with open(FINAL_MANIFEST, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"final_manifest.json is not valid JSON: {e}")

    assert "version" in data, "Missing 'version' in final_manifest.json"
    assert data["version"] == 2, f"Expected version 2, got {data.get('version')}"

    assert "artifacts" in data, "Missing 'artifacts' in final_manifest.json"
    artifacts = data["artifacts"]

    expected_items = ["item-1", "item-2"]
    for item in expected_items:
        assert item in artifacts, f"Missing {item} in artifacts"

    # Check item-1
    item1 = artifacts["item-1"]
    assert item1.get("file") == "builder/src/archiver.c", "Incorrect file for item-1"
    assert item1.get("category") == "source", "Incorrect category for item-1"
    expected_checksum_1 = compute_expected_checksum(item1["file"])
    assert item1.get("checksum") == expected_checksum_1, f"Incorrect checksum for item-1. Expected {expected_checksum_1}, got {item1.get('checksum')}"

    # Check item-2
    item2 = artifacts["item-2"]
    assert item2.get("file") == "builder/src/packager.c", "Incorrect file for item-2"
    assert item2.get("category") == "source", "Incorrect category for item-2"
    expected_checksum_2 = compute_expected_checksum(item2["file"])
    assert item2.get("checksum") == expected_checksum_2, f"Incorrect checksum for item-2. Expected {expected_checksum_2}, got {item2.get('checksum')}"