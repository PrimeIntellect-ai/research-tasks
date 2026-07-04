# test_final_state.py
import os
import json
import pytest
import requests

def test_http_api_fruit():
    url = "http://127.0.0.1:9000/api/stats?category=fruit"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200 for category=fruit, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    assert data.get("category") == "fruit", f"Expected category 'fruit', got {data.get('category')}"
    assert data.get("total_count") == 5, f"Expected total_count 5 for fruit, got {data.get('total_count')}"

def test_http_api_animal():
    url = "http://127.0.0.1:9000/api/stats?category=animal"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200 for category=animal, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    assert data.get("category") == "animal", f"Expected category 'animal', got {data.get('category')}"
    assert data.get("total_count") == 3, f"Expected total_count 3 for animal, got {data.get('total_count')}"

def test_http_api_nonexistent_category():
    url = "http://127.0.0.1:9000/api/stats?category=nonexistent_category_123"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    # Can be 404 or 200 with total_count 0
    if response.status_code == 200:
        try:
            data = response.json()
            assert data.get("total_count") == 0, f"Expected total_count 0 for nonexistent category, got {data.get('total_count')}"
        except json.JSONDecodeError:
            pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")
    else:
        assert response.status_code == 404, f"Expected status code 404 (or 200 with count 0) for nonexistent category, got {response.status_code}"

def test_etl_log_exists_and_valid():
    log_path = "/home/user/etl_project/logs/etl.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) >= 3, f"Expected at least 3 log lines in {log_path}, got {len(lines)}"

    parsed_logs = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        try:
            log_entry = json.loads(line)
            parsed_logs.append(log_entry)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {log_path} is not valid JSON: {line}")

    # Verify the structure has "step", "status", "records"
    for entry in parsed_logs:
        assert "step" in entry, f"Log entry missing 'step': {entry}"
        assert "status" in entry, f"Log entry missing 'status': {entry}"
        assert "records" in entry, f"Log entry missing 'records': {entry}"
        assert entry["status"] == "completed", f"Expected status 'completed', got {entry['status']}"