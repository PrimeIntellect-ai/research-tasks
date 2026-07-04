# test_final_state.py

import os
import json
import requests
import pytest

def test_api_reachable_and_metrics_exist():
    """Ensure the Analytics API is running on port 8080 and exposes metrics."""
    try:
        resp = requests.get("http://127.0.0.1:8080/metrics", timeout=5)
        assert resp.status_code == 200, f"API returned status code {resp.status_code} instead of 200."

        data = resp.json()
        assert "received_valid_count" in data, "Metrics JSON missing 'received_valid_count' key."
    except requests.RequestException as e:
        pytest.fail(f"API not reachable at http://127.0.0.1:8080/metrics. Did you fix the port and leave it running? Error: {e}")

def test_recovery_recall_threshold():
    """Calculate the recall metric and assert it meets the >= 0.98 threshold."""
    # 1. Get received valid count from API
    try:
        resp = requests.get("http://127.0.0.1:8080/metrics", timeout=5)
        received = resp.json().get("received_valid_count", 0)
    except Exception as e:
        pytest.fail(f"Could not fetch metrics from API to calculate recall: {e}")

    # 2. Get expected valid count from truth log
    truth_file = "/app/services/truth_log.json"
    assert os.path.exists(truth_file), f"Truth log file {truth_file} is missing."

    with open(truth_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse {truth_file} as JSON.")

    # Expected records are those with value >= 0.0
    expected = len([d for d in data if d.get("value", -1.0) >= 0.0])
    assert expected > 0, "Expected valid count is 0. Generator may not have run properly."

    # 3. Calculate and assert recall
    recall = received / expected
    assert recall >= 0.98, (
        f"Recall {recall:.4f} is below the 0.98 threshold. "
        f"Received {received} valid records, but expected {expected}."
    )