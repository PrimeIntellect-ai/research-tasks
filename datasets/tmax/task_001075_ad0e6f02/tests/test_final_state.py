# test_final_state.py
import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/binary_integrator"
AGENT_PATH = "/home/user/replicated_integrator.sh"
NUM_TESTS = 100

def test_agent_script_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent script missing at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    random.seed(42)

    for i in range(NUM_TESTS):
        r = random.uniform(5.0, 20.0)
        v = random.uniform(0.0, 2.0)
        dt = random.uniform(0.001, 0.1)
        steps = random.randint(10, 500)

        args = [f"{r:.6f}", f"{v:.6f}", f"{dt:.6f}", str(steps)]

        # Run oracle
        oracle_cmd = [ORACLE_PATH] + args
        try:
            oracle_result = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True, timeout=5)
            oracle_out = oracle_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {args}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {args}")

        # Run agent
        agent_cmd = [AGENT_PATH] + args
        try:
            agent_result = subprocess.run(agent_cmd, capture_output=True, text=True, check=True, timeout=5)
            agent_out = agent_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input {args}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input {args}")

        assert agent_out == oracle_out, (
            f"Output mismatch on test {i+1}/{NUM_TESTS}.\n"
            f"Inputs: r={args[0]}, v={args[1]}, dt={args[2]}, steps={args[3]}\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output:  '{agent_out}'"
        )