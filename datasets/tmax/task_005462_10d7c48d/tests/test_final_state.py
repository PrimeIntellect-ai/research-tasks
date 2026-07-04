# test_final_state.py
import os
import json
import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"

def test_processed_data_file_exists():
    file_path = "/home/user/processed_data.json"
    assert os.path.isfile(file_path), f"Expected processed data file at {file_path} does not exist."
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

def test_transcript_endpoint():
    url = f"{BASE_URL}/transcript"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /transcript is not valid JSON.")

    assert "transcript" in data, "Response JSON missing 'transcript' key."
    transcript = data["transcript"].lower()

    expected_words = ["alpha", "latency", "anomalies", "database"]
    for word in expected_words:
        assert word in transcript, f"Expected word '{word}' not found in transcript."

def test_stats_endpoint():
    url = f"{BASE_URL}/stats"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /stats is not valid JSON.")

    assert "latency_ci" in data, "Response JSON missing 'latency_ci' key."
    assert "database_ci" in data, "Response JSON missing 'database_ci' key."

    latency_ci = data["latency_ci"]
    database_ci = data["database_ci"]

    assert isinstance(latency_ci, list) and len(latency_ci) == 2, "'latency_ci' must be a list of two numbers."
    assert isinstance(database_ci, list) and len(database_ci) == 2, "'database_ci' must be a list of two numbers."

    for val in latency_ci + database_ci:
        assert isinstance(val, (int, float)), f"CI bounds must be numbers, got {type(val)}"

def test_search_endpoint():
    url = f"{BASE_URL}/search"
    payload = {"query": "how much did latency drop"}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /search is not valid JSON.")

    assert "match" in data, "Response JSON missing 'match' key."
    match = data["match"].lower()

    assert "latency decreased" in match, f"Expected 'latency decreased' in match, got '{data['match']}'"