# test_final_state.py

import os
import json
import pytest
import requests

def test_pipeline_status_log():
    log_file = "/home/user/pipeline_status.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."
    with open(log_file, "r") as f:
        content = f.read().strip()
    assert "READY" in content, f"Log file {log_file} does not contain the word 'READY'. Found: '{content}'"

def test_env_configuration():
    env_file = "/home/user/app/serving/.env"
    assert os.path.isfile(env_file), f"Environment file {env_file} is missing."
    with open(env_file, "r") as f:
        content = f.read()
    assert "CLEANER_URL=http://localhost:8080/data" in content, (
        f"Environment file {env_file} does not contain the correct CLEANER_URL. "
        f"Contents: {content}"
    )

def test_data_ingest_service():
    url = "http://localhost:8000/data.json"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to data_ingest service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 from {url}, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON: {response.text}")

    assert "raw" in data, f"Expected key 'raw' in response from {url}, got {data}"
    assert data["raw"] == "Hello, World! Data Science 123.", (
        f"Unexpected raw data from {url}: {data['raw']}"
    )

def test_cleaning_worker_service():
    url = "http://localhost:8080/data"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to cleaning_worker service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 from {url}, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON: {response.text}")

    expected_tokens = ["hello", "world", "data", "science", "123"]
    assert isinstance(data, list), f"Expected JSON array from {url}, got {type(data)}"
    assert data == expected_tokens, f"Expected tokens {expected_tokens} from {url}, got {data}"

def test_model_serving_service():
    url = "http://localhost:9000/predict"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to model_serving service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 from {url}, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON: {response.text}")

    assert "status" in data, f"Expected key 'status' in response from {url}, got {data}"
    assert data["status"] == "success", f"Expected status 'success' from {url}, got {data['status']}"
    assert "score" in data, f"Expected key 'score' in response from {url}, got {data}"

    expected_score = 42.0
    assert abs(data["score"] - expected_score) < 0.01, (
        f"Expected score close to {expected_score} from {url}, got {data['score']}"
    )