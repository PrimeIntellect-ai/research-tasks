# test_final_state.py

import os
import requests
import pytest

def test_token_file_recovered():
    token_path = "/home/user/geo_api/token.key"
    assert os.path.exists(token_path), f"Token file {token_path} is missing. Did you recover it from git history?"
    with open(token_path, "r") as f:
        content = f.read().strip()
    assert content == "sec_r3t_9942xyz", f"Token file content is incorrect. Expected 'sec_r3t_9942xyz', got '{content}'"

def test_api_process_endpoint():
    url = "http://127.0.0.1:8080/process"
    headers = {
        "Authorization": "Bearer sec_r3t_9942xyz",
        "Content-Type": "application/json"
    }
    payload = {
        "coords": [45.123456789, -122.987654321]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}. Is the server running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "result" in data, f"Response JSON missing 'result' key. Got: {data}"

    result = data["result"]
    assert isinstance(result, list), f"Expected 'result' to be a list, got {type(result)}"
    assert len(result) == 3, f"Expected 3 items in result array, got {len(result)}: {result}"

    assert result[0] == 45.123456789, f"First coordinate lost precision or is incorrect. Expected 45.123456789, got {result[0]}"
    assert result[1] == -122.987654321, f"Second coordinate lost precision or is incorrect. Expected -122.987654321, got {result[1]}"
    assert result[2] == 120, f"Math computation result is incorrect. Expected 120 (from compute_series(5)), got {result[2]}"