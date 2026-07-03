# test_final_state.py
import os
import json
import time
import requests
import numpy as np
import pytest

def test_nginx_config_updated():
    config_path = "/app/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"{config_path} does not exist"
    with open(config_path, "r") as f:
        content = f.read()
    assert "proxy_read_timeout 10s;" in content, "proxy_read_timeout is not set to 10s in nginx.conf"

def test_regression_test_script_exists():
    script_path = "/home/user/regression_test.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist"

def test_resolution_json_correct():
    json_path = "/home/user/resolution.json"
    assert os.path.isfile(json_path), f"{json_path} does not exist"
    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not a valid JSON file")

    assert "problematic_endpoint" in data, "Missing 'problematic_endpoint' in resolution.json"
    assert "root_cause_function" in data, "Missing 'root_cause_function' in resolution.json"

    assert data["problematic_endpoint"] == "/api/v1/search?q=test_prefix***", f"Incorrect problematic_endpoint: {data['problematic_endpoint']}"
    assert data["root_cause_function"].lower() == "keys", f"Incorrect root_cause_function: {data['root_cause_function']}"

def test_latency_metric_threshold():
    latencies = []
    for _ in range(100):
        start = time.time()
        try:
            resp = requests.get("http://127.0.0.1:8080/api/v1/search?q=test_prefix***", timeout=5)
            latencies.append((time.time() - start) * 1000)
            assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {e}")

    p95_latency = np.percentile(latencies, 95)
    assert p95_latency <= 100.0, f"P95 latency was {p95_latency:.2f}ms, which exceeds the threshold of 100.0ms."