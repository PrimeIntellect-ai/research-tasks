# test_final_state.py

import os
import json
import pytest
import requests

def test_server_executable_exists():
    """Test that the compiled C server executable exists."""
    server_path = "/home/user/server"
    assert os.path.isfile(server_path), f"The server executable {server_path} does not exist."
    assert os.access(server_path, os.X_OK), f"The file {server_path} is not executable."

def test_server_aggregate_endpoint():
    """Test the /aggregate endpoint with a sequence of words."""
    url = "http://127.0.0.1:8080/aggregate"

    # Test case 1 from the prompt
    words_1 = "dog cat dog fish dog cat bird bird"
    expected_1 = [3, 3, 3, 4, 3]

    try:
        resp_1 = requests.post(url, data=words_1, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert resp_1.status_code == 200, f"Expected status code 200, got {resp_1.status_code}"

    try:
        data_1 = json.loads(resp_1.text)
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {resp_1.text}")

    assert data_1 == expected_1, f"Expected {expected_1}, got {data_1}"

    # Test case 2: All unique
    words_2 = "a b c d e f"
    expected_2 = [4, 4, 4]

    resp_2 = requests.post(url, data=words_2, timeout=5)
    assert resp_2.status_code == 200
    assert json.loads(resp_2.text) == expected_2, f"Expected {expected_2}, got {resp_2.text}"

    # Test case 3: All same
    words_3 = "x x x x x"
    expected_3 = [1, 1]

    resp_3 = requests.post(url, data=words_3, timeout=5)
    assert resp_3.status_code == 200
    assert json.loads(resp_3.text) == expected_3, f"Expected {expected_3}, got {resp_3.text}"