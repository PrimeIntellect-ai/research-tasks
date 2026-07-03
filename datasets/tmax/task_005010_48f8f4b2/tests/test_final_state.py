# test_final_state.py

import os
import requests
import pytest

def test_hypothesis_script_exists():
    path = "/home/user/test_semver.py"
    assert os.path.isfile(path), f"File {path} does not exist"
    with open(path, "r") as f:
        content = f.read()
    assert "hypothesis" in content, f"File {path} does not seem to use the hypothesis library"

def test_server_sort_endpoint():
    url = "http://127.0.0.1:8888/sort"
    # Include a very long pre-release string to ensure the buffer overflow is fixed
    long_version = "1.0.0-super.long.prerelease.string.that.overflows.buffer.and.tests.the.fix"
    payload = {
        "versions": [
            "3.0.0",
            "1.0.0-rc.1",
            "1.0.0-beta",
            "2.0.0",
            long_version
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url} or request failed: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "sorted" in data, f"Expected 'sorted' key in response, got: {data}"

    expected_sorted = [
        "1.0.0-beta",
        "1.0.0-rc.1",
        long_version,
        "2.0.0",
        "3.0.0"
    ]
    assert data["sorted"] == expected_sorted, f"Expected sorted versions {expected_sorted}, got {data['sorted']}"

def test_server_diff_endpoint():
    url = "http://127.0.0.1:8888/diff"
    payload = {
        "base": ["1.2.3", "2.0.0"],
        "target": ["1.2.3", "3.0.0-alpha", "2.0.0", "4.0.0"]
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url} or request failed: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "diff" in data, f"Expected 'diff' key in response, got: {data}"

    expected_diff = ["3.0.0-alpha", "4.0.0"]
    assert data["diff"] == expected_diff, f"Expected diff {expected_diff}, got {data['diff']}"