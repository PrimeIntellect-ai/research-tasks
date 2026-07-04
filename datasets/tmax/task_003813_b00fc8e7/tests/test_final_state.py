# test_final_state.py

import os
import pytest
import requests

def test_hyperparameter_file_exists_and_correct():
    filepath = "/home/user/app/best_hyperparameter.txt"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse '{content}' as a float in {filepath}.")

    # The expected correct hyperparameter after fixing the data leak is 0.65
    assert abs(val - 0.65) < 0.01, f"Expected threshold around 0.65, but got {val}. The data leak might not be correctly fixed."

def test_server_unauthorized():
    url = "http://127.0.0.1:8080/retrieve"
    payload = {"query": "find me the main database cluster"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized when missing Auth header, got {response.status_code}"

def test_server_authorized_and_correct_response():
    url = "http://127.0.0.1:8080/retrieve"
    payload = {"query": "find me the main database cluster"}
    headers = {"Authorization": "Bearer ds_secret_token"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Failed to parse response as JSON. Response: {response.text}")

    assert "match_id" in data, f"Response JSON missing 'match_id' key. Response: {data}"
    assert "confidence" in data, f"Response JSON missing 'confidence' key. Response: {data}"

    assert data["match_id"] == "doc_042", f"Expected match_id 'doc_042', got {data['match_id']}"
    assert isinstance(data["confidence"], float) or isinstance(data["confidence"], int), "Confidence must be a number."