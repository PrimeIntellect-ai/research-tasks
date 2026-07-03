# test_final_state.py

import os
import ast
import hashlib
import requests
import pytest

def test_setup_py_syntax():
    """Verify that setup.py has valid Python syntax."""
    setup_path = "/app/test-util/setup.py"
    assert os.path.isfile(setup_path), f"File {setup_path} does not exist."
    with open(setup_path, "r") as f:
        content = f.read()
    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"setup.py still contains syntax errors: {e}")

def test_server_valid_request():
    """Verify that the server responds correctly to a valid request."""
    url = "http://127.0.0.1:9055/verify"
    token = "GO_MOCK_XYZ123"
    headers = {"Authorization": f"Bearer {token}"}

    expected_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server on port 9055: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.text.strip() == expected_hash, f"Expected body to be {expected_hash}, got {response.text}"

def test_server_invalid_request():
    """Verify that the server responds with 401 Unauthorized for missing/incorrect auth."""
    url = "http://127.0.0.1:9055/verify"

    # Missing auth
    try:
        response_missing = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server on port 9055: {e}")

    assert response_missing.status_code == 401, f"Expected status code 401 for missing auth, got {response_missing.status_code}"

    # Incorrect auth
    headers = {"Authorization": "Bearer WRONG_TOKEN"}
    try:
        response_wrong = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server on port 9055: {e}")

    assert response_wrong.status_code == 401, f"Expected status code 401 for incorrect auth, got {response_wrong.status_code}"