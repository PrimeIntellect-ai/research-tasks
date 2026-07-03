# test_final_state.py

import os
import requests
import pytest

def test_responder_source_exists():
    path = '/home/user/responder.c'
    assert os.path.isfile(path), f"The C source file {path} is missing."

def test_responder_binary_exists():
    path = '/home/user/responder'
    assert os.path.isfile(path), f"The compiled binary {path} is missing."
    assert os.access(path, os.X_OK), f"The compiled binary {path} is not executable."

def test_remediate_endpoint():
    url = "http://127.0.0.1:8080/remediate"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the responder service at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, but got {response.status_code}."

    expected_content = "SUCCESS: FLAG_PROC_LEAK_REMEDIATED_9921"
    actual_content = response.text.strip()

    assert expected_content in actual_content, (
        f"The response from the /remediate endpoint did not match the expected output.\n"
        f"Expected to contain: {expected_content}\n"
        f"Actual response: {actual_content}"
    )