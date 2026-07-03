# test_final_state.py
import json
import socket
import pytest
import requests

def get_redis_key(key):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect(('127.0.0.1', 6379))
        cmd = f"*2\r\n$3\r\nGET\r\n${len(key)}\r\n{key}\r\n"
        s.sendall(cmd.encode('utf-8'))
        resp = s.recv(4096).decode('utf-8')
    finally:
        s.close()

    lines = resp.split('\r\n')
    if len(lines) >= 2 and lines[0].startswith('$') and lines[0] != '$-1':
        return lines[1]
    return None

def test_redis_metadata():
    """Verify the model metadata in Redis."""
    val = get_redis_key("model:latest")
    assert val is not None, "Redis key 'model:latest' not found or empty."

    try:
        data = json.loads(val)
    except json.JSONDecodeError:
        pytest.fail(f"Redis value is not valid JSON: {val}")

    assert data.get("status") == "trained", f"Expected status 'trained', got {data.get('status')}"
    assert data.get("path") == "/home/user/artifacts/pipeline.joblib", f"Expected path '/home/user/artifacts/pipeline.joblib', got {data.get('path')}"

    # The median of memory_mb (1024, 2048, 4096, 512) is 1536.0
    imputed_memory = data.get("imputed_memory")
    assert imputed_memory in (1536, 1536.0), f"Expected imputed_memory to be 1536.0, got {imputed_memory}"

def test_http_valid_request():
    """Test A: Valid Request with all fields"""
    payload = {"cpu_usage": 50.0, "memory_mb": 2048, "disk_io": 200.0, "network_rx": 15.0}
    try:
        r = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=2.0)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to web service: {e}")

    assert r.status_code == 200, f"Expected HTTP 200, got {r.status_code}. Response: {r.text}"

    resp_json = r.json()
    assert "latency_pred" in resp_json, "Response missing 'latency_pred'"
    assert "anomaly_pred" in resp_json, "Response missing 'anomaly_pred'"
    assert isinstance(resp_json["latency_pred"], float), "latency_pred must be a float"
    assert isinstance(resp_json["anomaly_pred"], int), "anomaly_pred must be an int"

def test_http_schema_out_of_bounds_cpu():
    """Test B: Schema Enforcement - Out of bounds cpu_usage"""
    payload = {"cpu_usage": 150.0, "memory_mb": 2048, "disk_io": 200.0}
    try:
        r = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=2.0)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to web service: {e}")

    assert r.status_code in (400, 422), f"Expected HTTP 400 or 422 for out-of-bounds cpu_usage, got {r.status_code}. Response: {r.text}"

def test_http_schema_invalid_memory_type():
    """Test C: Schema Enforcement - Invalid memory_mb value"""
    payload = {"cpu_usage": 50.0, "memory_mb": -100, "disk_io": 200.0}
    try:
        r = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=2.0)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to web service: {e}")

    assert r.status_code in (400, 422), f"Expected HTTP 400 or 422 for invalid memory_mb, got {r.status_code}. Response: {r.text}"

def test_http_missing_values_and_defaulting():
    """Test D: Missing Value Handling & Defaulting"""
    payload = {"cpu_usage": 80.0, "disk_io": 1500.0}
    try:
        r = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=2.0)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to web service: {e}")

    assert r.status_code == 200, f"Expected HTTP 200 for payload with missing optional fields, got {r.status_code}. Response: {r.text}"

    resp_json = r.json()
    assert "latency_pred" in resp_json, "Response missing 'latency_pred'"
    assert "anomaly_pred" in resp_json, "Response missing 'anomaly_pred'"
    assert isinstance(resp_json["latency_pred"], float), "latency_pred must be a float"
    assert isinstance(resp_json["anomaly_pred"], int), "anomaly_pred must be an int"