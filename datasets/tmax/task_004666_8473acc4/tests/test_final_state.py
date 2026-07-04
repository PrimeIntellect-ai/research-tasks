# test_final_state.py

import os
import subprocess
import random
import pytest

def test_config_env_updated():
    config_path = "/app/emitter/config.env"
    assert os.path.isfile(config_path), f"File {config_path} is missing."
    with open(config_path, "r") as f:
        content = f.read()
    assert "REDIS_HOST=127.0.0.1" in content, "config.env REDIS_HOST not updated to 127.0.0.1."
    assert "REDIS_PORT=6379" in content, "config.env REDIS_PORT not updated to 6379."

def test_listener_port_updated():
    listener_path = "/app/webhook/listener.py"
    assert os.path.isfile(listener_path), f"File {listener_path} is missing."
    with open(listener_path, "r") as f:
        content = f.read()
    assert "8081" in content, "listener.py port not updated to 8081."

def test_worker_script_exists():
    worker_path = "/home/user/worker.sh"
    assert os.path.isfile(worker_path), f"File {worker_path} is missing."

def test_analyze_fuzz_equivalence():
    oracle_path = "/opt/oracle/analyze_oracle"
    agent_path = "/home/user/analyze"

    assert os.path.isfile(agent_path), f"Agent binary {agent_path} is missing."
    assert os.access(agent_path, os.X_OK), f"Agent binary {agent_path} is not executable."

    random.seed(42)
    bases = ['A', 'C', 'T', 'G']

    for i in range(100):
        length = random.randint(10, 5000)
        seq = "".join(random.choices(bases, k=length))

        oracle_proc = subprocess.run([oracle_path, seq], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_path, seq], capture_output=True, text=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input length {length}"
        assert agent_proc.returncode == 0, f"Agent failed on input length {length}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, f"Mismatch on input {seq[:50]}... (len {length}). Expected: {oracle_out[:50]}..., Got: {agent_out[:50]}..."