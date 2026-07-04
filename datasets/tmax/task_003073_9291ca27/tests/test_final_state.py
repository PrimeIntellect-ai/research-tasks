# test_final_state.py
import os
import json
import pytest
import requests

def test_bad_commit_txt():
    bad_commit_path = "/home/user/bad_commit.txt"
    secret_path = "/app/anomaly_pipeline/.secret_bad_commit"

    assert os.path.isfile(bad_commit_path), f"File {bad_commit_path} does not exist."
    assert os.path.isfile(secret_path), f"Secret file {secret_path} does not exist."

    with open(bad_commit_path, "r") as f:
        bad_commit = f.read().strip()

    with open(secret_path, "r") as f:
        secret_commit = f.read().strip()

    assert bad_commit == secret_commit, f"Bad commit hash in {bad_commit_path} is incorrect."

def test_config_json_port():
    config_path = "/app/anomaly_pipeline/config.json"
    assert os.path.isfile(config_path), f"File {config_path} does not exist."

    with open(config_path, "r") as f:
        config = json.load(f)

    assert config.get("redis_port") == 6379, "redis_port in config.json is not 6379."

def test_api_response_json():
    api_response_path = "/home/user/api_response.json"
    assert os.path.isfile(api_response_path), f"File {api_response_path} does not exist."

    with open(api_response_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {api_response_path} does not contain valid JSON.")

    assert "status" in data, "API response JSON missing 'status' key."

def test_api_endpoint():
    url = "http://127.0.0.1:8080/api/v1/analyze"
    headers = {"Authorization": "Bearer IT-SUPPORT-AUTH-992"}
    payload = {"series_id": "verify_456"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"API response is not valid JSON. Response: {response.text}")

    assert data.get("status") == "converged", f"Expected status 'converged', got {data.get('status')}."
    assert "variance" in data, "API response missing 'variance'."
    assert isinstance(data["variance"], (float, int)), "API response 'variance' is not a number."