# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_health_script():
    health_script = "/home/user/health.sh"
    assert os.path.isfile(health_script), f"{health_script} does not exist"
    assert os.access(health_script, os.X_OK), f"{health_script} is not executable"

    result = subprocess.run([health_script], capture_output=True, text=True)
    assert result.returncode == 0, f"{health_script} failed with exit code {result.returncode}, stderr: {result.stderr}"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/rusty-slugger-oracle"
    agent_path = "/home/user/backend-bin"

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} not found"
    assert os.access(oracle_path, os.X_OK), f"Oracle binary {oracle_path} not executable"

    assert os.path.isfile(agent_path), f"Agent binary {agent_path} not found"
    assert os.access(agent_path, os.X_OK), f"Agent binary {agent_path} not executable"

    random.seed(42)
    printable = string.printable

    for i in range(100):
        length = random.randint(5, 50)
        input_str = "".join(random.choice(printable) for _ in range(length))

        oracle_res = subprocess.run([oracle_path, input_str], capture_output=True, text=True)
        agent_res = subprocess.run([agent_path, input_str], capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input {repr(input_str)}"
        assert agent_res.returncode == 0, f"Agent failed on input {repr(input_str)}"

        assert agent_res.stdout == oracle_res.stdout, (
            f"Output mismatch on input {repr(input_str)}:\n"
            f"Expected (Oracle): {repr(oracle_res.stdout)}\n"
            f"Actual (Agent): {repr(agent_res.stdout)}"
        )