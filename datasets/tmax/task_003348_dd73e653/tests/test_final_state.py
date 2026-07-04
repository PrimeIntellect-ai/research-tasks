# test_final_state.py
import os
import re
import requests
import pytest

def get_expected_results(batch_name):
    # Compute expected results dynamically based on the CSV files
    csv_path = f"/home/user/data/{batch_name}.csv"
    if not os.path.exists(csv_path):
        return None

    scores = []
    anomalies = 0
    with open(csv_path, 'r') as f:
        lines = f.read().strip().split('\n')
        if len(lines) > 1:
            for line in lines[1:]:
                parts = line.split(',')
                if len(parts) == 4:
                    v1, v2, v3 = float(parts[1]), float(parts[2]), float(parts[3])
                    score = (0.5 * v1) + (1.2 * v2) + (0.8 * v3)
                    scores.append(score)
                    if score > 5.0:
                        anomalies += 1

    if not scores:
        return {"batch": batch_name, "average_score": 0.0, "anomalies": 0}

    avg_score = sum(scores) / len(scores)
    return {"batch": batch_name, "average_score": round(avg_score, 2), "anomalies": anomalies}

def test_api_test_batch():
    expected = get_expected_results("test_batch")
    assert expected is not None, "test_batch.csv is missing"

    try:
        response = requests.get("http://127.0.0.1:8080/process?batch=test_batch", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "batch" in data, "Missing 'batch' in JSON response"
    assert "average_score" in data, "Missing 'average_score' in JSON response"
    assert "anomalies" in data, "Missing 'anomalies' in JSON response"

    assert data["batch"] == expected["batch"], f"Expected batch {expected['batch']}, got {data['batch']}"
    assert abs(data["average_score"] - expected["average_score"]) < 1e-2, f"Expected average_score {expected['average_score']}, got {data['average_score']}"
    assert data["anomalies"] == expected["anomalies"], f"Expected anomalies {expected['anomalies']}, got {data['anomalies']}"

def test_api_batch1():
    expected = get_expected_results("batch1")
    assert expected is not None, "batch1.csv is missing"

    try:
        response = requests.get("http://127.0.0.1:8080/process?batch=batch1", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data["batch"] == expected["batch"], f"Expected batch {expected['batch']}, got {data['batch']}"
    assert abs(data["average_score"] - expected["average_score"]) < 1e-2, f"Expected average_score {expected['average_score']}, got {data['average_score']}"
    assert data["anomalies"] == expected["anomalies"], f"Expected anomalies {expected['anomalies']}, got {data['anomalies']}"

def test_tracking_log():
    log_path = "/home/user/tracking.log"
    assert os.path.exists(log_path), f"Tracking log {log_path} does not exist"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content, "Tracking log is empty"

    lines = content.split('\n')

    # Format: [<timestamp>] BATCH=<batch_name> AVG=<average_score> ANOMALIES=<count>
    # Timestamp: ISO 8601 UTC time, e.g., 2023-10-25T14:30:00Z
    pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\] BATCH=(\w+) AVG=([0-9.]+) ANOMALIES=(\d+)$")

    found_test_batch = False
    found_batch1 = False

    for line in lines:
        match = pattern.match(line)
        assert match, f"Log line does not match expected format: {line}"

        batch = match.group(1)
        avg = float(match.group(2))
        anom = int(match.group(3))

        expected = get_expected_results(batch)
        if expected:
            # The script might not round the log output to 2 decimals, so we check loose equality or exact
            assert abs(avg - expected["average_score"]) < 0.1, f"Log average score {avg} does not match expected {expected['average_score']} for batch {batch}"
            assert anom == expected["anomalies"], f"Log anomalies {anom} does not match expected {expected['anomalies']} for batch {batch}"

            if batch == "test_batch":
                found_test_batch = True
            elif batch == "batch1":
                found_batch1 = True

    assert found_test_batch, "test_batch was not found in tracking.log"
    assert found_batch1, "batch1 was not found in tracking.log"