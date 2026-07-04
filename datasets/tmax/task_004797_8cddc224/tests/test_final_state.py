# test_final_state.py

import os
import math
import json
import socket
import pytest
import requests

def get_ground_truth_mean(pdb_path):
    ca_coords = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM  ") and line[12:16].strip() == "CA":
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                ca_coords.append((x, y, z))

    distances = []
    for i in range(1, len(ca_coords)):
        d = math.sqrt(sum((a - b)**2 for a, b in zip(ca_coords[i], ca_coords[i-1])))
        distances.append(d)

    smoothed = []
    for i in range(len(distances)):
        prev_idx = max(0, i-1)
        next_idx = min(len(distances)-1, i+1)
        s = (distances[prev_idx] + distances[i] + distances[next_idx]) / 3.0
        smoothed.append(s)

    mean_val = sum(smoothed) / len(smoothed)
    return mean_val

def test_unauthenticated_request():
    """Test that requests without the proper Bearer token return 401 Unauthorized."""
    url = "http://127.0.0.1:9000/prepare_training_data"
    payload = {"pdb_id": "1XYZ", "num_bootstrap_samples": 100}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Go API server: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for unauthenticated request, got {response.status_code}. Response: {response.text}"

def test_authenticated_request_and_values():
    """Test the authenticated request and validate the calculated values."""
    url = "http://127.0.0.1:9000/prepare_training_data"
    headers = {"Authorization": "Bearer ml_prep_token_2024"}
    payload = {"pdb_id": "1XYZ", "num_bootstrap_samples": 1000}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Go API server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "status" in data and data["status"] == "success", "Response JSON missing 'status': 'success'"
    assert "mean" in data, "Response JSON missing 'mean'"
    assert "ci_lower" in data, "Response JSON missing 'ci_lower'"
    assert "ci_upper" in data, "Response JSON missing 'ci_upper'"

    expected_mean = get_ground_truth_mean("/app/data/1XYZ.pdb")

    assert math.isclose(data["mean"], expected_mean, rel_tol=1e-4), \
        f"Calculated mean {data['mean']} does not match expected mean {expected_mean}"

    # CI bounds should be somewhat close to the mean, usually within a small margin for a large sample
    # We allow a generous tolerance since bootstrap is stochastic
    assert data["ci_lower"] <= data["mean"] <= data["ci_upper"], "Mean should be within the confidence interval"
    assert math.isclose(data["ci_lower"], expected_mean, abs_tol=0.5), f"ci_lower {data['ci_lower']} is too far from mean"
    assert math.isclose(data["ci_upper"], expected_mean, abs_tol=0.5), f"ci_upper {data['ci_upper']} is too far from mean"

def test_redis_cache():
    """Test that the CI results are cached in Redis."""
    # Send a raw RESP command to redis
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(("127.0.0.1", 6379))

        # Construct RESP GET command
        cmd = "*2\r\n$3\r\nGET\r\n$15\r\nspectro_ci_1XYZ\r\n"
        s.sendall(cmd.encode('utf-8'))

        response = s.recv(4096).decode('utf-8')
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect to Redis and retrieve key: {e}")

    # Redis bulk string reply starts with '$' followed by length, then \r\n, then data
    assert response.startswith("$"), f"Expected bulk string reply from Redis, got: {response}"

    if response.startswith("$-1"):
        pytest.fail("Key 'spectro_ci_1XYZ' not found in Redis.")

    lines = response.split("\r\n")
    if len(lines) >= 2:
        data_str = lines[1]
        try:
            ci_array = json.loads(data_str)
            assert isinstance(ci_array, list) and len(ci_array) == 2, "Cached data should be an array of two floats [ci_lower, ci_upper]"
        except ValueError:
            # If it's not JSON, maybe it's comma separated or something similar, but JSON array is expected
            assert "[" in data_str and "]" in data_str, f"Cached data does not look like an array: {data_str}"