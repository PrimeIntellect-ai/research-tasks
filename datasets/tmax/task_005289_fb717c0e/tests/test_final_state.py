# test_final_state.py

import os
import random
import subprocess
import tempfile
import pytest

def test_config_env():
    """Verify that config.env contains the correct SENSOR_HOST and SENSOR_PORT."""
    config_path = "/home/user/config.env"
    assert os.path.isfile(config_path), f"{config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    assert "SENSOR_HOST=localhost" in content, "SENSOR_HOST=localhost not found in config.env"
    assert "SENSOR_PORT=9001" in content, "SENSOR_PORT=9001 not found in config.env"

def test_aggregate_script_exists_and_executable():
    """Verify that aggregate.sh exists and is executable."""
    script_path = "/home/user/aggregate.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_fuzz_equivalence():
    """Fuzz equivalence test comparing the agent's script to the oracle."""
    oracle_path = "/app/oracle_aggregate"
    agent_path = "/home/user/aggregate.sh"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} missing."

    random.seed(42)

    for i in range(200):
        num_lines = random.randint(10, 1000)

        # Generate random data
        data = []
        for _ in range(num_lines):
            x = random.randint(0, 100000)
            y = random.uniform(-1000.0, 1000.0)
            data.append((x, y))

        # Shuffle to ensure sorting is required
        random.shuffle(data)

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            for x, y in data:
                tmp.write(f"{x} {y:.6f}\n")
            tmp_path = tmp.name

        try:
            # Run oracle
            oracle_proc = subprocess.run([oracle_path, tmp_path], capture_output=True, text=True)
            assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"
            oracle_out = oracle_proc.stdout.strip()

            # Run agent
            agent_proc = subprocess.run([agent_path, tmp_path], capture_output=True, text=True)
            assert agent_proc.returncode == 0, f"Agent script failed on input {i}. Stderr: {agent_proc.stderr}"
            agent_out = agent_proc.stdout.strip()

            assert agent_out == oracle_out, (
                f"Mismatch on fuzz input {i} (lines={num_lines}).\n"
                f"Expected (Oracle): {oracle_out}\n"
                f"Got (Agent): {agent_out}\n"
                f"First few lines of input:\n"
                + "\n".join([f"{x} {y:.6f}" for x, y in data[:5]])
            )
        finally:
            os.remove(tmp_path)