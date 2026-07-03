# test_final_state.py
import json
import random
import subprocess
import os
import pytest
import urllib.request

def test_pipeline_fuzz_equivalence():
    oracle_path = "/app/oracle_pipeline.py"
    agent_path = "/home/user/pipeline.py"

    assert os.path.exists(oracle_path), f"Oracle path {oracle_path} does not exist."
    assert os.path.exists(agent_path), f"Agent path {agent_path} does not exist."

    # Seed some redis data to test the multiplier logic
    try:
        import redis
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        r.ping()
        for i in range(1, 10000, 100):
            r.set(f"multiplier_{i}", random.uniform(0.1, 5.0))
    except Exception as e:
        pytest.fail(f"Could not connect to Redis to set test data. Is Redis running on 127.0.0.1:6379? Error: {e}")

    # Check if Flask API is up
    try:
        req = urllib.request.Request('http://127.0.0.1:5000/predict', data=b'{"feature": 1.0}', headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200
    except Exception as e:
        pytest.fail(f"Flask API is not running or not responding correctly at 127.0.0.1:5000. Error: {e}")

    rng = random.Random(42)
    N = 100

    for _ in range(N):
        user_id = rng.randint(1, 10000)
        v1 = rng.uniform(-50.0, 50.0)
        v2 = rng.uniform(-50.0, 50.0)

        input_data = {
            "user_id": user_id,
            "v1": v1,
            "v2": v2
        }
        input_str = json.dumps(input_data)

        oracle_cmd = ["python3", oracle_path, input_str]
        agent_cmd = ["python3", agent_path, input_str]

        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True, timeout=5)
            oracle_output = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {input_str}:\n{e.stderr}")

        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, check=True, timeout=5)
            agent_output = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input {input_str}:\n{e.stderr}")

        assert agent_output == oracle_output, (
            f"Mismatch on input: {input_str}\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output:  {agent_output}"
        )