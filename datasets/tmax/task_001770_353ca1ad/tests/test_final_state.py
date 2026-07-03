# test_final_state.py

import os
import json
import random
import subprocess
import urllib.request
import pytest

def test_redis_config_updated():
    with open("/home/user/investigation/redis.conf", "r") as f:
        content = f.read()
    assert "requirepass Sup3rS3cr3tT3l3m3try!" in content, "redis.conf does not contain the correct requirepass directive."

def test_broker_config_updated():
    with open("/home/user/investigation/broker-repo/config.json", "r") as f:
        config = json.load(f)
    assert config.get("redis_pass") == "Sup3rS3cr3tT3l3m3try!", "Broker config.json does not have the correct redis_pass."
    assert config.get("worker_port") == 9000, "Broker config.json does not have the correct worker_port."

def test_worker_binary_exists():
    assert os.path.isfile("/home/user/investigation/worker"), "Compiled worker binary is missing."
    assert os.access("/home/user/investigation/worker", os.X_OK), "Compiled worker is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_worker"
    agent_path = "/home/user/investigation/worker"

    assert os.path.isfile(oracle_path), "Oracle binary missing."
    assert os.path.isfile(agent_path), "Agent binary missing."

    random.seed(42)
    N = 100

    for i in range(N):
        payload = []
        for _ in range(100):
            lat = random.uniform(-90.0, 90.0)
            lon = random.uniform(-180.0, 180.0)
            alt = random.uniform(0.0, 10000.0)
            payload.append({"lat": lat, "lon": lon, "alt": alt})

        input_data = json.dumps(payload).encode('utf-8')

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on input {i}"
        assert agent_proc.stdout == oracle_proc.stdout, f"Stdout mismatch on input {i}.\nInput: {input_data}\nOracle: {oracle_proc.stdout}\nAgent: {agent_proc.stdout}"

def test_e2e_flow():
    payload = [{"lat": 37.7749, "lon": -122.4194, "alt": 10.0}, {"lat": 34.0522, "lon": -118.2437, "alt": 20.0}]
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request("http://127.0.0.1:8080/process", data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            res_data = response.read()
            assert len(res_data) > 0, "Empty response from broker."
    except Exception as e:
        pytest.fail(f"E2E request failed: {e}")