# test_final_state.py

import os
import requests
import pytest
import time

def test_makefile_typo_fixed():
    makefile_path = '/app/jo-1.9/Makefile.in'
    assert os.path.isfile(makefile_path), f"The file {makefile_path} is missing."

    with open(makefile_path, 'r') as f:
        content = f.read()

    assert "LDFALGS = @LDFLAGS@" not in content, f"The typo 'LDFALGS = @LDFLAGS@' was not fixed in {makefile_path}."
    assert "LDFLAGS = @LDFLAGS@" in content, f"The expected 'LDFLAGS = @LDFLAGS@' was not found in {makefile_path}."

def test_jo_binary_compiled():
    jo_binary = '/app/jo-1.9/jo'
    assert os.path.isfile(jo_binary), f"The compiled binary {jo_binary} is missing."
    assert os.access(jo_binary, os.X_OK), f"The file {jo_binary} is not executable."

def test_server_response():
    url = "http://127.0.0.1:8080/api/status"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}."

    content_type = response.headers.get('Content-Type', '')
    assert 'application/json' in content_type, f"Expected Content-Type 'application/json', got '{content_type}'."

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    expected_data = {
        "build": "pass",
        "deploy": "fail",
        "integration": "pass",
        "lint": "pass",
        "unit": "pass"
    }

    assert data == expected_data, f"Expected JSON payload {expected_data}, got {data}."