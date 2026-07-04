# test_final_state.py

import os
import csv
import requests
import pytest

API_BASE_URL = "http://127.0.0.1:8080"

def get_json(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        pytest.fail(f"Failed to fetch {endpoint} from API: {e}")

def test_api_stats():
    """Test the /stats endpoint."""
    data = get_json("/stats")

    assert "lower_bound" in data, "Missing 'lower_bound' in /stats response"
    assert "upper_bound" in data, "Missing 'upper_bound' in /stats response"
    assert "mean_inference_sec" in data, "Missing 'mean_inference_sec' in /stats response"

    lower_bound = float(data["lower_bound"])
    upper_bound = float(data["upper_bound"])
    mean_inference_sec = float(data["mean_inference_sec"])

    assert upper_bound > lower_bound, f"Upper bound ({upper_bound}) must be greater than lower bound ({lower_bound})"
    assert mean_inference_sec > 0, "Mean inference time must be positive"

def test_api_anomalies():
    """Test the /anomalies endpoint."""
    data = get_json("/anomalies")

    assert "anomalous_frames" in data, "Missing 'anomalous_frames' in /anomalies response"
    anomalous_frames = data["anomalous_frames"]

    assert isinstance(anomalous_frames, list), "'anomalous_frames' must be a list"
    for frame in anomalous_frames:
        assert isinstance(frame, int), "All items in 'anomalous_frames' must be integers"

def test_api_validation():
    """Test the /validation endpoint and verify precision logic."""
    # Fetch anomalies
    anomalies_data = get_json("/anomalies")
    anomalous_frames = anomalies_data.get("anomalous_frames", [])

    # Fetch validation
    validation_data = get_json("/validation")
    assert "precision" in validation_data, "Missing 'precision' in /validation response"
    reported_precision = float(validation_data["precision"])

    # Verify precision against CSV
    csv_path = "/home/user/sensor_logs.csv"
    assert os.path.isfile(csv_path), f"CSV file missing at {csv_path}"

    sensor_active_map = {}
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensor_active_map[int(row["timestamp_sec"])] = int(row["sensor_active"])

    if not anomalous_frames:
        expected_precision = 0.0
    else:
        true_positives = sum(1 for frame in anomalous_frames if sensor_active_map.get(frame, 0) == 1)
        expected_precision = true_positives / len(anomalous_frames)

    assert 0.0 <= reported_precision <= 1.0, "Precision must be between 0.0 and 1.0"
    assert abs(reported_precision - expected_precision) < 1e-4, \
        f"Reported precision {reported_precision} does not match expected precision {expected_precision} based on returned anomalies."