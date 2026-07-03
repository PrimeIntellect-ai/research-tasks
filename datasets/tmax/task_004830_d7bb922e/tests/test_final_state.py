# test_final_state.py
import os
import json
import urllib.request
import pytest

def test_config_env_secret():
    config_path = "/home/user/app/config.env"
    assert os.path.exists(config_path), f"File {config_path} is missing."
    with open(config_path, "r") as f:
        content = f.read()
    assert "API_SECRET=d34db33f_s3cr3t99" in content, f"config.env does not contain the correct API_SECRET. Found: {content}"

def test_ingester_executable_exists():
    ingester_path = "/home/user/app/ingester/ingester"
    assert os.path.exists(ingester_path), f"Executable {ingester_path} is missing. Did you compile the C code?"
    assert os.access(ingester_path, os.X_OK), f"File {ingester_path} is not executable."

def test_recovery_yield_metric():
    try:
        req = urllib.request.Request("http://localhost:5000/metrics")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            valid_processed = data.get("processed_count", 0)
    except Exception as e:
        pytest.fail(f"Failed to retrieve metrics from API on port 5000. Ensure both the API and Redis are running. Error: {e}")

    yield_rate = valid_processed / 1000.0
    assert yield_rate >= 0.95, f"Recovery yield {yield_rate} is below the required threshold of 0.95 (Processed: {valid_processed}/1000 valid records)"