# test_final_state.py

import os
import subprocess
import random
import pytest

AGENT_SRC = "/home/user/diffusion_solver.c"
AGENT_BIN = "/home/user/diffusion_solver"
ORACLE_BIN = "/app/reference_oracle"

def test_source_file_exists():
    assert os.path.exists(AGENT_SRC), f"Source file {AGENT_SRC} does not exist."
    assert os.path.isfile(AGENT_SRC), f"{AGENT_SRC} is not a file."

def test_binary_exists_and_executable():
    assert os.path.exists(AGENT_BIN), f"Executable {AGENT_BIN} does not exist."
    assert os.path.isfile(AGENT_BIN), f"{AGENT_BIN} is not a file."
    assert os.access(AGENT_BIN, os.X_OK), f"{AGENT_BIN} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BIN), f"Oracle {ORACLE_BIN} does not exist."
    assert os.access(ORACLE_BIN, os.X_OK), f"Oracle {ORACLE_BIN} is not executable."

    random.seed(42)
    N_TESTS = 100

    for i in range(N_TESTS):
        T = random.randint(10, 1000)
        initial_conditions = ",".join(f"{random.uniform(0.0, 1.0):.4f}" for _ in range(10))

        args = [str(T), initial_conditions]

        try:
            oracle_res = subprocess.run([ORACLE_BIN] + args, capture_output=True, text=True, timeout=5)
            oracle_out = oracle_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: T={T}, init={initial_conditions}")
        except Exception as e:
            pytest.fail(f"Oracle failed to run: {e}")

        try:
            agent_res = subprocess.run([AGENT_BIN] + args, capture_output=True, text=True, timeout=5)
            agent_out = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input: T={T}, init={initial_conditions}")
        except Exception as e:
            pytest.fail(f"Agent failed to run: {e}")

        assert oracle_res.returncode == 0, f"Oracle returned non-zero exit code {oracle_res.returncode} on input: T={T}, init={initial_conditions}"

        if agent_res.returncode != 0:
            pytest.fail(f"Agent returned non-zero exit code {agent_res.returncode} on input: T={T}, init={initial_conditions}\nAgent stderr: {agent_res.stderr}")

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on test case {i+1}/{N_TESTS}.\n"
                f"Input T: {T}\n"
                f"Input IC: {initial_conditions}\n"
                f"Expected (Oracle): {oracle_out}\n"
                f"Got (Agent):       {agent_out}"
            )