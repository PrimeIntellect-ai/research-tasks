# test_final_state.py

import os
import requests
import pytest
import time

def test_parsed_fstab_file():
    """Verify that the parsed fstab configuration file was created correctly."""
    fstab_path = "/app/parsed_fstab.conf"
    assert os.path.isfile(fstab_path), f"File not found: {fstab_path}"

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    expected_fstab = "UUID=55aa-88bb /restore/db xfs rw,noatime 0 2"
    assert content == expected_fstab, f"Expected fstab content '{expected_fstab}', but got '{content}'"

def test_http_server_health_endpoint():
    """Verify the /health endpoint of the HTTP server."""
    url = "http://127.0.0.1:9050/health"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type to be application/json"

    try:
        json_data = response.json()
    except ValueError:
        pytest.fail("Response body is not valid JSON")

    assert json_data == {"status": "ok"}, f"Expected JSON {{'status': 'ok'}}, but got {json_data}"

def test_http_server_key_endpoint():
    """Verify the /key endpoint of the HTTP server."""
    url = "http://127.0.0.1:9050/key"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    content = response.text.strip()
    expected_key = "AlphaOmega-992"
    assert content == expected_key, f"Expected key '{expected_key}', but got '{content}'"

def test_http_server_fstab_endpoint():
    """Verify the /fstab endpoint of the HTTP server."""
    url = "http://127.0.0.1:9050/fstab"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    content = response.text.strip()
    expected_fstab = "UUID=55aa-88bb /restore/db xfs rw,noatime 0 2"
    assert content == expected_fstab, f"Expected fstab '{expected_fstab}', but got '{content}'"