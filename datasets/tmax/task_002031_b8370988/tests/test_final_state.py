# test_final_state.py

import os
import subprocess
import requests
import time
import pytest
from pathlib import Path

def test_filter_script_corpus():
    script_path = "/home/user/filter.py"
    assert os.path.isfile(script_path), f"Missing filter script: {script_path}"

    clean_dir = Path("/app/tests/corpus/clean")
    evil_dir = Path("/app/tests/corpus/evil")

    clean_files = list(clean_dir.glob("*.json"))
    evil_files = list(evil_dir.glob("*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run(["python3", script_path, str(cf)], capture_output=True, text=True)
        if res.returncode != 0 or "CLEAN" not in res.stdout:
            clean_failed.append(cf.name)

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run(["python3", script_path, str(ef)], capture_output=True, text=True)
        if res.returncode != 1 or "EVIL" not in res.stdout:
            evil_failed.append(ef.name)

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_env_configured():
    env_path = "/app/data_app/.env"
    assert os.path.isfile(env_path), "Missing .env file"
    with open(env_path, "r") as f:
        content = f.read()

    assert "REDIS_HOST=127.0.0.1" in content, "REDIS_HOST not set correctly in .env"
    assert "REDIS_PORT=6379" in content, "REDIS_PORT not set correctly in .env"
    assert "FILTER_SCRIPT=/home/user/filter.py" in content, "FILTER_SCRIPT not set correctly in .env"

def test_services_running_and_proxying():
    # Test end-to-end flow via Nginx
    clean_payload = [{"sensor_id": "S1", "timestamp": 1620000000, "value": 10.5}, {"sensor_id": "S1", "timestamp": 1620000001, "value": 10.6}]
    evil_payload = [{"sensor_id": "S1", "timestamp": 1620000000, "value": 100.5}, {"sensor_id": "S1", "timestamp": 1620000001, "value": 100.6}]

    try:
        # Test clean payload
        res_clean = requests.post("http://127.0.0.1:8080/upload", json=clean_payload, timeout=5)
        assert res_clean.status_code == 200, f"Expected HTTP 200 for clean payload, got {res_clean.status_code}"

        # Test evil payload
        res_evil = requests.post("http://127.0.0.1:8080/upload", json=evil_payload, timeout=5)
        assert res_evil.status_code == 400, f"Expected HTTP 400 for evil payload, got {res_evil.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx proxy on port 8080: {e}")