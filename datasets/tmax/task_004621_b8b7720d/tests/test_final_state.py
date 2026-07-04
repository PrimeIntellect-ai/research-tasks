# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle_integrator"
AGENT_SCRIPT = "/home/user/integrate_model.py"

def test_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary is not executable at {ORACLE_PATH}"

    random.seed(42)
    N = 500

    for _ in range(N):
        t_end = round(random.uniform(0.1, 15.0), 4)
        num_steps = random.randint(10, 2000)

        t_end_str = f"{t_end:.4f}"
        num_steps_str = str(num_steps)

        # Run oracle
        oracle_cmd = [ORACLE_PATH, t_end_str, num_steps_str]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on inputs: {t_end_str} {num_steps_str}"
        oracle_out = oracle_res.stdout.strip()

        # Run agent
        agent_cmd = ["python3", AGENT_SCRIPT, t_end_str, num_steps_str]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on inputs: {t_end_str} {num_steps_str}\nStderr: {agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on inputs t_end={t_end_str}, num_steps={num_steps_str}.\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output:  '{agent_out}'"
        )