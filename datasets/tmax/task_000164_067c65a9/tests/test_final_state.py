# test_final_state.py

import os
import subprocess
import random
import pytest

def test_vendored_package_fixed():
    """Verify that the vendored package's go.mod has been fixed to remove 'go 1.99'."""
    go_mod_path = "/app/graph/go.mod"
    assert os.path.isfile(go_mod_path), f"{go_mod_path} is missing."
    with open(go_mod_path, "r") as f:
        content = f.read()
    assert "go 1.99" not in content, "The go.mod in /app/graph still contains the invalid 'go 1.99' version."
    assert "go 1." in content, "The go.mod in /app/graph does not seem to contain a valid Go version directive."

def test_agent_executable_exists():
    """Verify that the agent's executable is built and present."""
    agent_path = "/home/user/simulate"
    assert os.path.isfile(agent_path), f"Agent executable {agent_path} is missing."
    assert os.access(agent_path, os.X_OK), f"Agent executable {agent_path} is not executable."

def test_fuzz_equivalence():
    """Verify that the agent's program matches the oracle program exactly on random inputs."""
    agent_path = "/home/user/simulate"
    oracle_path = "/opt/oracle/simulate_oracle"

    assert os.path.isfile(oracle_path), f"Oracle executable {oracle_path} is missing."

    random.seed(12345)

    for i in range(50):
        length = random.randint(20, 100)
        seq = "".join(random.choices(["A", "C", "G", "T"], k=length))
        seed = random.randint(1, 10000)

        oracle_cmd = [oracle_path, seq, str(seed)]
        agent_cmd = [agent_path, seq, str(seed)]

        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True, timeout=5)
            oracle_out = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input seq={seq}, seed={seed}. Error: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input seq={seq}, seed={seed}.")

        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, check=True, timeout=5)
            agent_out = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input seq={seq}, seed={seed}. Error: {e.stderr}\nStdout: {e.stdout}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input seq={seq}, seed={seed}.")

        assert agent_out == oracle_out, (
            f"Output mismatch on fuzzing round {i+1}!\n"
            f"Input seq: {seq}\n"
            f"Input seed: {seed}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )