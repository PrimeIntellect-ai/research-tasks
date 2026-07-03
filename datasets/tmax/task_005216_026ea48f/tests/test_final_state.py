# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def generate_random_input():
    length = random.randint(0, 100)
    data = []
    for _ in range(length):
        row = {}
        # 10% chance to drop f1
        if random.random() > 0.1:
            # 10% chance for null
            row["f1"] = random.uniform(-10.0, 10.0) if random.random() > 0.1 else None
        # 10% chance to drop f2
        if random.random() > 0.1:
            row["f2"] = random.uniform(-10.0, 10.0) if random.random() > 0.1 else None
        data.append(row)
    return data

def test_fuzz_equivalence():
    random.seed(42)
    oracle_path = "/app/oracle_preprocessor.py"
    agent_path = "/home/user/preprocessor.py"

    assert os.path.isfile(agent_path), f"Agent script {agent_path} is missing."
    assert os.access(agent_path, os.X_OK), f"Agent script {agent_path} is not executable."

    for i in range(500):
        input_data = generate_random_input()
        input_str = json.dumps(input_data)

        oracle_proc = subprocess.run([oracle_path], input=input_str, text=True, capture_output=True)
        agent_proc = subprocess.run(["python3", agent_path], input=input_str, text=True, capture_output=True)

        assert agent_proc.returncode == 0, f"Agent script failed on input: {input_str}\nError: {agent_proc.stderr}"

        try:
            oracle_out = json.loads(oracle_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle script output invalid JSON on input: {input_str}\nOutput: {oracle_proc.stdout}")

        try:
            agent_out = json.loads(agent_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Agent script output invalid JSON on input: {input_str}\nOutput: {agent_proc.stdout}")

        assert agent_out == oracle_out, f"Mismatch on input {input_str}\nExpected: {oracle_out}\nGot: {agent_out}"

def test_worker_fixed():
    worker_path = "/app/worker.py"
    assert os.path.isfile(worker_path), f"{worker_path} is missing."

    with open(worker_path, "r") as f:
        content = f.read()

    assert "port=6379" in content.replace(" ", ""), "Worker Redis port not fixed to 6379 in /app/worker.py"
    assert "http://localhost:5000/log_metric" in content, "Worker API URL not fixed to http://localhost:5000/log_metric in /app/worker.py"