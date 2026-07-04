# test_final_state.py

import pytest
import requests

def test_process_endpoint():
    url = "http://127.0.0.1:8080/process"

    # Input data
    # t=30 is a duplicate config_id ("A") and should be dropped.
    # t=50 is out of order in the list, should be sorted.
    payload = [
        {"timestamp": 50, "cpu": None, "mem": None, "config_id": "D"},
        {"timestamp": 10, "cpu": 2.0, "mem": 100.0, "config_id": "A"},
        {"timestamp": 20, "cpu": None, "mem": None, "config_id": "B"},
        {"timestamp": 30, "cpu": 99.0, "mem": 999.0, "config_id": "A"},
        {"timestamp": 40, "cpu": 8.0, "mem": 200.0, "config_id": "C"}
    ]

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service or request timed out: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(data, list), f"Expected response to be a JSON array, got {type(data).__name__}"
    assert len(data) == 4, f"Expected 4 records after deduplication, got {len(data)}"

    expected = [
        {
            "timestamp": 10,
            "cpu_imputed": 2.0,
            "mem_imputed": 100.0,
            "cpu_rolling_avg": 2.0,
            "mem_rolling_avg": 100.0
        },
        {
            "timestamp": 20,
            "cpu_imputed": 4.0,
            "mem_imputed": 133.33,
            "cpu_rolling_avg": 3.0,
            "mem_rolling_avg": 116.67
        },
        {
            "timestamp": 40,
            "cpu_imputed": 8.0,
            "mem_imputed": 200.0,
            "cpu_rolling_avg": 4.67,
            "mem_rolling_avg": 144.44
        },
        {
            "timestamp": 50,
            "cpu_imputed": 8.0,
            "mem_imputed": 200.0,
            "cpu_rolling_avg": 6.67,
            "mem_rolling_avg": 177.78
        }
    ]

    for i, exp in enumerate(expected):
        actual = data[i]
        assert actual.get("timestamp") == exp["timestamp"], f"Record {i}: expected timestamp {exp['timestamp']}, got {actual.get('timestamp')}"

        for key in ["cpu_imputed", "mem_imputed", "cpu_rolling_avg", "mem_rolling_avg"]:
            actual_val = actual.get(key)
            assert actual_val is not None, f"Record {i}: missing key '{key}'"
            assert isinstance(actual_val, (int, float)), f"Record {i}: '{key}' should be a number"
            assert round(actual_val, 2) == exp[key], f"Record {i}: expected {key} == {exp[key]}, got {actual_val}"