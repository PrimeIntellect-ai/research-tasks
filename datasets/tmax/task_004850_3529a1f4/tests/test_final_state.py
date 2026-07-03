# test_final_state.py

import os
import random
import subprocess

def test_predictor_fuzz_equivalence():
    agent_script = "/home/user/predictor.sh"
    oracle_script = "/app/oracle_predictor.sh"

    assert os.path.isfile(agent_script), f"{agent_script} does not exist. Did you create it?"
    assert os.access(agent_script, os.X_OK), f"{agent_script} is not executable. Did you run chmod +x?"

    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} is missing."
    assert os.access(oracle_script, os.X_OK), f"Oracle script {oracle_script} is not executable."

    # Generate 100 random inputs as specified in the fuzz distribution
    random.seed(42)
    inputs = [random.randint(0, 1000000000) for _ in range(100)]

    for val in inputs:
        str_val = str(val)

        agent_res = subprocess.run([agent_script, str_val], capture_output=True, text=True)
        oracle_res = subprocess.run([oracle_script, str_val], capture_output=True, text=True)

        assert agent_res.returncode == 0, f"Agent script failed on input {str_val}. Stderr: {agent_res.stderr}"
        assert oracle_res.returncode == 0, f"Oracle script failed on input {str_val}. Stderr: {oracle_res.stderr}"

        agent_out = agent_res.stdout.strip()
        oracle_out = oracle_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on input CPU_Load={str_val}.\n"
            f"Expected (Oracle): '{oracle_out}'\n"
            f"Got (Agent):       '{agent_out}'\n"
            "Check your linear regression calculations, rounding, and formula application."
        )