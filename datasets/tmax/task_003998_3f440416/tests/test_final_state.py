# test_final_state.py

import os
import requests
import pytest

def test_merged_manifest_exists_and_sorted():
    path = "/app/merged_manifest.csv"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"File {path} is empty"
    assert lines[0] == "ArtifactID,Name,Version", "Header is missing or incorrect"

    data_lines = lines[1:]
    assert data_lines == sorted(data_lines), "Data rows are not sorted alphabetically"

    # Check that all artifacts from parts 1-3 are present
    content = "\n".join(lines)
    assert "A100,Backend,1.0.0" in content
    assert "A101,Database,1.5.2" in content
    assert "A102,Auth,1.1.1" in content
    assert "A103,Frontend,2.1.0" in content
    assert "A104,Logger,1.0.5" in content
    assert "A105,Cache,3.0.0" in content

def test_final_manifest_exists_and_patched():
    path = "/app/final_manifest.csv"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_content = """ArtifactID,Name,Version
A100,Backend,1.0.0
A101,Database,1.6.0
A102,Auth,1.1.1
A103,Frontend,2.1.0
A104,Logger,1.1.0
A105,Cache,3.0.0"""

    assert content == expected_content, f"Content of {path} does not match expected patched output"

def test_processed_logs_exists_and_not_empty():
    path = "/app/processed_logs.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    assert len(content) > 0, f"File {path} is empty"

def test_server_auth_success():
    url = "http://127.0.0.1:8080/manifest"
    headers = {"Authorization": "Bearer REL-8492-SEC"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200 OK, got {response.status_code}"

    with open("/app/final_manifest.csv", 'r') as f:
        expected_body = f.read()

    assert response.text.strip() == expected_body.strip(), "Response body does not match /app/final_manifest.csv"

def test_server_auth_missing():
    url = "http://127.0.0.1:8080/manifest"

    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 401, f"Expected status 401 Unauthorized for missing auth, got {response.status_code}"

def test_server_auth_invalid():
    url = "http://127.0.0.1:8080/manifest"
    headers = {"Authorization": "Bearer INVALID-TOKEN"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 401, f"Expected status 401 Unauthorized for invalid auth, got {response.status_code}"