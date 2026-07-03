# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_token_file_contents():
    token_path = "/home/user/build_token.txt"
    assert os.path.isfile(token_path), f"Token file {token_path} is missing."
    with open(token_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == "MEM_SEC_0xFA9B", f"Expected token 'MEM_SEC_0xFA9B' in {token_path}, but got '{content}'"

def test_http_service_health():
    url = "http://127.0.0.1:8080/health"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    expected_data = {"status": "running", "token": "MEM_SEC_0xFA9B"}
    assert data == expected_data, f"Expected JSON {expected_data}, but got {data}"

def test_processor_tests_pass():
    test_file = "/home/user/build/test_processor.py"
    assert os.path.isfile(test_file), f"Test file {test_file} is missing."

    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest failed for {test_file}. Output:\n{result.stdout}\n{result.stderr}"