# test_final_state.py

import os
import json
import hashlib
import subprocess
import pytest

REPORT_PATH = "/home/user/report.json"
PATCH_PATH = "/home/user/patches/fix_1.3.1.patch"
BINARY_PATH = "/home/user/rust_processor/target/release/rust_processor"

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_report_json_exists_and_valid():
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"
    with open(REPORT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    expected_keys = {"resolved_version", "patch_checksum", "average_time_ms", "mock_hit"}
    assert expected_keys.issubset(data.keys()), f"Report JSON is missing required keys. Found: {list(data.keys())}"

def test_report_resolved_version():
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)
    assert data["resolved_version"] == "1.3.1", f"Expected resolved_version to be '1.3.1', got '{data.get('resolved_version')}'"

def test_report_patch_checksum():
    assert os.path.isfile(PATCH_PATH), f"Patch file missing: {PATCH_PATH}"
    expected_hash = get_sha256(PATCH_PATH)

    with open(REPORT_PATH, "r") as f:
        data = json.load(f)
    assert data["patch_checksum"] == expected_hash, f"Expected patch_checksum to be '{expected_hash}', got '{data.get('patch_checksum')}'"

def test_report_mock_hit():
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)
    assert data["mock_hit"] is True, f"Expected mock_hit to be true, got {data.get('mock_hit')}"

def test_report_average_time_ms():
    with open(REPORT_PATH, "r") as f:
        data = json.load(f)
    avg_time = data.get("average_time_ms")
    assert isinstance(avg_time, (int, float)), "average_time_ms must be a number"
    assert avg_time > 0.0, f"Expected average_time_ms to be > 0.0, got {avg_time}"

def test_rust_binary_compiled():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"