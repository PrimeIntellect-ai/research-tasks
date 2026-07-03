# test_final_state.py

import os
import json
import pytest
import requests

def test_master_ip_file():
    ip_file = "/home/user/master_ip.txt"
    assert os.path.isfile(ip_file), f"File {ip_file} does not exist."
    with open(ip_file, "r") as f:
        content = f.read().strip()
    assert content == "10.42.15.99", f"Expected IP '10.42.15.99' in {ip_file}, found '{content}'."

def test_symlink_loop_removed():
    loop_symlink = "/home/user/repo_data/v1/loop_dir"
    assert not os.path.exists(loop_symlink) and not os.path.islink(loop_symlink), \
        f"The infinite loop symlink {loop_symlink} should be removed."

def test_regular_files_intact():
    files = [
        "/home/user/repo_data/v1/bin/artifact-a.bin",
        "/home/user/repo_data/v1/bin/artifact-b.bin",
        "/home/user/repo_data/v2/bin/artifact-c.bin",
        "/home/user/repo_data/v2/bin/artifact-d.bin",
        "/home/user/repo_data/readme.txt"
    ]
    for f in files:
        assert os.path.isfile(f) and not os.path.islink(f), f"Regular file {f} is missing or was modified to a symlink."

def test_valid_symlink_intact():
    symlink_path = "/home/user/repo_data/latest-c"
    target_path = "/home/user/repo_data/v2/bin/artifact-c.bin"
    assert os.path.islink(symlink_path), f"Valid symlink {symlink_path} was removed or modified."
    assert os.readlink(symlink_path) == target_path, f"Valid symlink {symlink_path} points to incorrect target."

def test_go_api_service():
    url = "http://127.0.0.1:8080/api/status"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}."

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    expected_data = {
        "master_ip": "10.42.15.99",
        "artifact_count": 5
    }

    assert data == expected_data, f"API returned incorrect JSON payload. Expected {expected_data}, got {data}."