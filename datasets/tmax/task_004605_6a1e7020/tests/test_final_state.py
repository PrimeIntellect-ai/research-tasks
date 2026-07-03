# test_final_state.py

import os
import requests
import pytest

EXPECTED_VERSIONS = [
    "v0.9.5",
    "v1.0.1",
    "v1.1.0",
    "v2.0.0-rc.1",
    "v2.0.0",
    "v3.1.2"
]

def test_extracted_versions_file():
    """Test that the extracted_versions.txt file exists and contains the correct sorted versions."""
    file_path = "/home/user/project_files/extracted_versions.txt"
    assert os.path.isfile(file_path), f"Output file is missing: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    versions = [line.strip() for line in content if line.strip()]
    assert versions == EXPECTED_VERSIONS, f"Extracted versions do not match expected. Found: {versions}"

def test_api_latest_version():
    """Test that the REST API returns the correct latest version."""
    url = "http://127.0.0.1:8080/api/versions/latest"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "latest" in data, "Response JSON missing 'latest' key"
    assert data["latest"] == "v3.1.2", f"Expected latest version 'v3.1.2', got '{data['latest']}'"

def test_api_newer_than():
    """Test that the REST API correctly filters versions newer than a query parameter."""
    url = "http://127.0.0.1:8080/api/versions/newer_than?v=1.1.0"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "versions" in data, "Response JSON missing 'versions' key"

    expected_newer = ["v2.0.0-rc.1", "v2.0.0", "v3.1.2"]
    assert data["versions"] == expected_newer, f"Expected versions {expected_newer}, got {data['versions']}"