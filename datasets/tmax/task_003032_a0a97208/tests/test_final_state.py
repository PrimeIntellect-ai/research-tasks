# test_final_state.py

import os
import random
import subprocess
import pytest

def test_load_gen_log():
    log_path = "/home/user/load_gen.log"
    assert os.path.isfile(log_path), f"Log file {log_path} not found. Did the services run?"
    with open(log_path, "r") as f:
        content = f.read()
    assert "Flow Complete" in content, f"'Flow Complete' not found in {log_path}. The services might still be misconfigured."

def test_analyze_metrics_fuzz_equivalence():
    agent_script = "/home/user/analyze_metrics.sh"
    oracle_script = "/opt/oracle/analyze_metrics_oracle"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} not found."
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable. Run chmod +x."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} not found."

    random.seed(42)
    for i in range(100):
        # Generate 10 random floats between 0.01 and 100.00 with 2 decimal precision
        args = [f"{random.uniform(0.01, 100.00):.2f}" for _ in range(10)]

        agent_res = subprocess.run([agent_script] + args, capture_output=True, text=True)
        oracle_res = subprocess.run([oracle_script] + args, capture_output=True, text=True)

        assert agent_res.returncode == 0, f"Agent script failed on input: {' '.join(args)}\nStderr: {agent_res.stderr}"
        assert oracle_res.returncode == 0, f"Oracle script failed on input: {' '.join(args)}\nStderr: {oracle_res.stderr}"

        agent_out = agent_res.stdout.strip()
        oracle_out = oracle_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on fuzz iteration {i+1} with input: {' '.join(args)}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent):       {agent_out}"
        )