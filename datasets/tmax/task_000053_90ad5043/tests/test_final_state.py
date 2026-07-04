# test_final_state.py

import os
import json
import pytest

def test_valid_files_moved():
    expected_paths = [
        "/home/user/organized/1.2/linux/amd64/worker_v1.2.3_linux_amd64.bin",
        "/home/user/organized/2.0/windows/amd64/worker_v2.0.0-alpha_windows_amd64.bin",
        "/home/user/organized/2.0/linux/amd64/worker_v2.0.1_linux_amd64.bin",
        "/home/user/organized/2.1/darwin/arm64/worker_v2.1.0-rc.1_darwin_arm64.bin"
    ]
    for path in expected_paths:
        assert os.path.isfile(path), f"Valid file was not moved to the expected location: {path}"

def test_invalid_files_not_moved():
    invalid_files = [
        "/home/user/artifacts/worker_v1.3.0_linux_arm64.bin",
        "/home/user/artifacts/worker_v1.2.4_darwin_amd64.bin"
    ]
    for path in invalid_files:
        assert os.path.isfile(path), f"Invalid file should not have been moved, but is missing from source: {path}"

def test_latest_version_file():
    path = "/home/user/latest_version.txt"
    assert os.path.isfile(path), f"Latest version file is missing: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "2.0.1", f"Expected latest version to be '2.0.1', but got '{content}'"

def test_mock_env_json():
    path = "/home/user/organized/2.0/linux/amd64/mock_env.json"
    assert os.path.isfile(path), f"Mock env file is missing: {path}"
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    expected_data = {"test_mode": True, "version": "2.0.1"}
    assert data == expected_data, f"Mock env file content is incorrect. Expected {expected_data}, got {data}"