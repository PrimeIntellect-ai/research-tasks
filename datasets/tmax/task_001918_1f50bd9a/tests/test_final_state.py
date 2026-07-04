# test_final_state.py
import os
import requests
import pytest
import unicodedata

AUTH_HEADER = {"Authorization": "Bearer ds_secret_token"}
BASE_URL = "http://127.0.0.1:8000"

def test_cron_schedule_file():
    path = "/home/user/cron_schedule.txt"
    assert os.path.exists(path), f"File {path} does not exist"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "0 2 * * *", f"Expected cron schedule '0 2 * * *', got '{content}'"

def test_api_auth_required():
    try:
        resp = requests.get(f"{BASE_URL}/api/config", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}: {e}")
    assert resp.status_code == 401, f"Expected 401 Unauthorized when missing auth header, got {resp.status_code}"

def test_api_config():
    try:
        resp = requests.get(f"{BASE_URL}/api/config", headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}: {e}")
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    data = resp.json()
    assert data.get("cron") == "0 2 * * *", f"Incorrect cron in config: {data.get('cron')}"
    assert data.get("strata_size") == 2, f"Incorrect strata_size in config: {data.get('strata_size')}"
    assert data.get("window") == 3, f"Incorrect window in config: {data.get('window')}"

def test_api_data():
    try:
        resp = requests.get(f"{BASE_URL}/api/data", headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}: {e}")
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    data = resp.json()
    assert isinstance(data, list), "Expected a JSON list of records"
    assert len(data) == 4, f"Expected 4 records after stratified sampling, got {len(data)}"

    # Expected data
    expected = [
        {"id": 1, "category": "A", "raw_text": unicodedata.normalize('NFKC', "café"), "value": 10.0, "rolling_avg": 10.0},
        {"id": 2, "category": "B", "raw_text": unicodedata.normalize('NFKC', "tést"), "value": 15.0, "rolling_avg": 12.5},
        {"id": 3, "category": "A", "raw_text": unicodedata.normalize('NFKC', "fußball"), "value": 20.0, "rolling_avg": 15.0},
        {"id": 4, "category": "B", "raw_text": unicodedata.normalize('NFKC', "æther"), "value": 25.0, "rolling_avg": 20.0}
    ]

    for i, exp in enumerate(expected):
        record = data[i]
        assert record.get("id") == exp["id"], f"Row {i}: Expected id {exp['id']}, got {record.get('id')}"
        assert record.get("category") == exp["category"], f"Row {i}: Expected category {exp['category']}, got {record.get('category')}"
        assert record.get("raw_text") == exp["raw_text"], f"Row {i}: Expected raw_text {exp['raw_text']}, got {record.get('raw_text')}"
        assert record.get("value") == exp["value"], f"Row {i}: Expected value {exp['value']}, got {record.get('value')}"
        assert record.get("rolling_avg") == exp["rolling_avg"], f"Row {i}: Expected rolling_avg {exp['rolling_avg']}, got {record.get('rolling_avg')}"