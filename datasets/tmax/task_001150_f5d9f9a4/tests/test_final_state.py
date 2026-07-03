# test_final_state.py
import os
import subprocess
import random
import pytest

def test_auto_deploy_success():
    script_path = "/home/user/auto_deploy.py"
    assert os.path.isfile(script_path), f"Missing file: {script_path}"

    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"auto_deploy.py failed with exit code {result.returncode}.\nStderr: {result.stderr}\nStdout: {result.stdout}"

    output = result.stdout + result.stderr
    assert "Deployment successful" in output, "auto_deploy.py did not cause the legacy deploy script to emit the 'Deployment successful' message."

def test_auth_signer_fuzz_equivalence():
    agent_script = "/home/user/auth_signer.py"
    oracle_bin = "/app/auth_signer"

    assert os.path.isfile(agent_script), f"Missing file: {agent_script}"
    assert os.path.isfile(oracle_bin), f"Missing oracle binary: {oracle_bin}"

    random.seed(42)
    # The truth specifies 5000 iterations between 1600000000 and 1800000000
    inputs = [str(random.randint(1600000000, 1800000000)) for _ in range(5000)]

    for val in inputs:
        oracle_res = subprocess.run([oracle_bin, val], capture_output=True, text=True)
        agent_res = subprocess.run(["python3", agent_script, val], capture_output=True, text=True)

        assert agent_res.returncode == 0, f"Agent script failed on input {val}. Stderr: {agent_res.stderr}"
        assert agent_res.stdout == oracle_res.stdout, (
            f"Mismatch on input {val}.\n"
            f"Expected output: {repr(oracle_res.stdout)}\n"
            f"Agent output: {repr(agent_res.stdout)}"
        )