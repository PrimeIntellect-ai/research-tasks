# test_final_state.py

import os
import random
import subprocess
import tempfile
import pytest
import h5py

ORACLE_PATH = "/app/profiler_sim"
AGENT_PATH = "/home/user/solution.py"
NUM_ITERATIONS = 100

def test_solution_exists():
    assert os.path.exists(AGENT_PATH), f"Agent solution not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent solution {AGENT_PATH} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable"

    random.seed(42)

    for i in range(NUM_ITERATIONS):
        x0 = random.uniform(0.1, 2.0)
        v0 = random.uniform(0.1, 2.0)
        dt_base = random.uniform(0.1, 2.0)

        with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            with h5py.File(tmp_path, "w") as f:
                f.create_dataset("/initial_state", data=[x0, v0, dt_base], dtype="float64")

            # Run oracle
            oracle_res = subprocess.run([ORACLE_PATH, tmp_path], capture_output=True, text=True)
            assert oracle_res.returncode == 0, f"Oracle failed on iteration {i} with input {[x0, v0, dt_base]}"
            oracle_out = oracle_res.stdout.strip()

            # Run agent
            agent_res = subprocess.run(["python3", AGENT_PATH, tmp_path], capture_output=True, text=True)
            assert agent_res.returncode == 0, f"Agent script failed on iteration {i} with input {[x0, v0, dt_base]}\nStderr: {agent_res.stderr}"
            agent_out = agent_res.stdout.strip()

            assert oracle_out == agent_out, (
                f"Mismatch on iteration {i} with input [x0={x0}, v0={v0}, dt_base={dt_base}].\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output: {agent_out}"
            )
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)