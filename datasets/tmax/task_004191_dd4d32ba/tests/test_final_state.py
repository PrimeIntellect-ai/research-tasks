# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
ENDPOINT = f"{BASE_URL}/api/search"
VALID_TOKEN = "astro-query-2024"
HEADERS = {"X-Research-Token": VALID_TOKEN}

def test_missing_auth():
    payload = {"category": "pulsar", "min_score": 0.0, "page": 1, "limit": 10}
    try:
        response = requests.post(ENDPOINT, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing token, got {response.status_code}"

def test_invalid_auth():
    payload = {"category": "pulsar", "min_score": 0.0, "page": 1, "limit": 10}
    headers = {"X-Research-Token": "wrong-token"}
    response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=5)
    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {response.status_code}"

def test_valid_query_pulsar():
    payload = {"category": "pulsar", "min_score": 0.0, "page": 1, "limit": 10}
    response = requests.post(ENDPOINT, json=payload, headers=HEADERS, timeout=5)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Body: {response.text}"

    data = response.json()
    assert data["page"] == 1
    assert data["limit"] == 10
    assert data["total_filtered_results"] == 2

    results = data["results"]
    assert len(results) == 2

    # Check sorting: score DESC
    assert results[0]["id"] == "obs_002"
    assert results[0]["score"] == 31.5
    assert results[1]["id"] == "obs_001"
    assert results[1]["score"] == 27.75

def test_pagination():
    payload = {"category": "pulsar", "min_score": 0.0, "page": 2, "limit": 1}
    response = requests.post(ENDPOINT, json=payload, headers=HEADERS, timeout=5)
    assert response.status_code == 200

    data = response.json()
    assert data["page"] == 2
    assert data["limit"] == 1
    assert data["total_filtered_results"] == 2

    results = data["results"]
    assert len(results) == 1
    assert results[0]["id"] == "obs_001"

def test_filtering_min_score():
    payload = {"category": "pulsar", "min_score": 30.0, "page": 1, "limit": 10}
    response = requests.post(ENDPOINT, json=payload, headers=HEADERS, timeout=5)
    assert response.status_code == 200

    data = response.json()
    assert data["total_filtered_results"] == 1
    assert len(data["results"]) == 1
    assert data["results"][0]["id"] == "obs_002"

def test_sql_injection_prevention():
    # If parameterized queries are used, this should return 0 results (no category matches the literal string)
    payload = {"category": "pulsar' OR 1=1 --", "min_score": 0.0, "page": 1, "limit": 10}
    response = requests.post(ENDPOINT, json=payload, headers=HEADERS, timeout=5)

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    data = response.json()
    assert data["total_filtered_results"] == 0, "SQL injection succeeded! Parameterized queries were not used correctly."
    assert len(data["results"]) == 0