# test_final_state.py

import json
import math
import socket
import pytest
import requests

NGINX_URL = "http://127.0.0.1:8080/api/stats"
AUTH_HEADER = {"Authorization": "Bearer secret-ml-token-99"}

def get_redis_lrange(key: str) -> list:
    """Fetch a list from Redis using a raw socket, avoiding third-party redis-py dependency."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect(('127.0.0.1', 6379))
        cmd = f"*4\r\n$6\r\nLRANGE\r\n${len(key)}\r\n{key}\r\n$1\r\n0\r\n$2\r\n-1\r\n"
        s.sendall(cmd.encode('utf-8'))

        fp = s.makefile('rb')
        line = fp.readline()
        if not line.startswith(b'*'):
            raise ValueError(f"Unexpected Redis response: {line}")

        count = int(line[1:].strip())
        if count == -1:
            return []

        res = []
        for _ in range(count):
            length_line = fp.readline()
            length = int(length_line[1:].strip())
            data = fp.read(length)
            res.append(data.decode('utf-8'))
            fp.read(2)  # consume \r\n
        return res
    finally:
        s.close()

def compute_expected_stats(raw_data: list) -> dict:
    group_a = []
    group_b = []

    for item in raw_data:
        obj = json.loads(item)
        if obj.get("group") == "A":
            group_a.append(obj["score"])
        elif obj.get("group") == "B":
            group_b.append(obj["score"])

    n_a = len(group_a)
    n_b = len(group_b)

    mean_a = sum(group_a) / n_a
    mean_b = sum(group_b) / n_b

    var_a = sum((x - mean_a) ** 2 for x in group_a) / (n_a - 1)
    var_b = sum((x - mean_b) ** 2 for x in group_b) / (n_b - 1)

    diff = mean_b - mean_a
    se = math.sqrt(var_b / n_b + var_a / n_a)

    ci_lower = diff - 1.96 * se
    ci_upper = diff + 1.96 * se

    return {
        "mean_A": mean_a,
        "mean_B": mean_b,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper
    }

def test_unauthorized_access():
    """Test that accessing the endpoint without the correct token returns 401."""
    try:
        response = requests.get(NGINX_URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx reverse proxy at {NGINX_URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_authorized_access_and_stats():
    """Test that accessing the endpoint with the correct token returns 200 and correct stats."""
    try:
        response = requests.get(NGINX_URL, headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx reverse proxy at {NGINX_URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK with correct token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got invalid JSON: {response.text}")

    required_keys = {"mean_A", "mean_B", "p_value", "ci_lower", "ci_upper"}
    assert required_keys.issubset(data.keys()), f"Response JSON missing required keys. Found: {list(data.keys())}"

    # Fetch data from Redis and compute expected values
    try:
        raw_telemetry = get_redis_lrange("raw_telemetry")
    except Exception as e:
        pytest.fail(f"Failed to fetch data from Redis: {e}")

    assert len(raw_telemetry) > 0, "Redis list 'raw_telemetry' is empty. Was populate_redis.py run?"

    expected_stats = compute_expected_stats(raw_telemetry)

    # Assert computed values are within 1e-4
    assert math.isclose(data["mean_A"], expected_stats["mean_A"], abs_tol=1e-4), \
        f"mean_A mismatch: expected {expected_stats['mean_A']}, got {data['mean_A']}"

    assert math.isclose(data["mean_B"], expected_stats["mean_B"], abs_tol=1e-4), \
        f"mean_B mismatch: expected {expected_stats['mean_B']}, got {data['mean_B']}"

    assert math.isclose(data["ci_lower"], expected_stats["ci_lower"], abs_tol=1e-4), \
        f"ci_lower mismatch: expected {expected_stats['ci_lower']}, got {data['ci_lower']}"

    assert math.isclose(data["ci_upper"], expected_stats["ci_upper"], abs_tol=1e-4), \
        f"ci_upper mismatch: expected {expected_stats['ci_upper']}, got {data['ci_upper']}"

    # p_value should be a valid probability
    assert isinstance(data["p_value"], float), "p_value must be a float"
    assert 0.0 <= data["p_value"] <= 1.0, f"p_value must be between 0 and 1, got {data['p_value']}"