# test_final_state.py

import os
import sys
import pytest

def test_test_api_py_exists_and_uses_hypothesis():
    test_file = "/home/user/api/test_api.py"
    assert os.path.isfile(test_file), f"{test_file} does not exist."
    with open(test_file, "r") as f:
        content = f.read()
    assert "hypothesis" in content, f"{test_file} does not use hypothesis."
    assert "TestClient" in content, f"{test_file} does not use TestClient."

def test_test_results_log_exists_and_passed():
    log_file = "/home/user/api/test_results.log"
    assert os.path.isfile(log_file), f"{log_file} does not exist."
    with open(log_file, "r") as f:
        content = f.read().lower()
    assert "passed" in content or "100%" in content, f"Test results log does not indicate successful test execution."

def test_main_py_fixed():
    # We need to test if main.py can be imported and works correctly
    sys.path.insert(0, "/home/user/api")
    try:
        from main import app
    except Exception as e:
        pytest.fail(f"Failed to import main.py. Is the library loading fixed? Error: {e}")

    try:
        from fastapi.testclient import TestClient
    except ImportError:
        pytest.fail("fastapi.testclient could not be imported. Are dependencies installed?")

    client = TestClient(app)
    response = client.post("/evaluate", json={"expression": "10+20"})
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert "result" in data, "Response JSON missing 'result' key"
    assert data["result"] == 30.0, f"Expected result 30.0, got {data['result']}"

    response2 = client.post("/evaluate", json={"expression": "15+2+99"})
    assert response2.status_code == 200
    assert response2.json()["result"] == 116.0