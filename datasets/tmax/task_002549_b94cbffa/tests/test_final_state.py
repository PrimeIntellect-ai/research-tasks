# test_final_state.py
import os
import random
import subprocess
import pytest

def test_binary_compiled():
    binary_path = "/app/sod-graph-checker-1.1.0/bin/check_sod"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing. Did you fix the Makefile and run make?"
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."

def test_agent_script_exists():
    script_path = "/home/user/audit_user.sh"
    assert os.path.isfile(script_path), f"Wrapper script {script_path} is missing."
    assert os.access(script_path, os.X_OK) or os.access(script_path, os.R_OK), f"Wrapper script {script_path} cannot be read/executed."

def test_fuzz_equivalence():
    oracle_path = "/usr/local/bin/oracle_audit.sh"
    agent_path = "/home/user/audit_user.sh"

    assert os.path.isfile(oracle_path), f"Oracle script {oracle_path} is missing."

    random.seed(42)
    uids = random.sample(range(1000, 1100), 25)

    for uid in uids:
        # Run oracle
        oracle_cmd = ["bash", oracle_path, str(uid)]
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on uid {uid} with stderr: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_cmd = ["bash", agent_path, str(uid)]
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_proc.returncode == 0, f"Agent script failed on uid {uid} with stderr: {agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        # Compare
        assert oracle_out == agent_out, (
            f"Mismatch on uid {uid}.\n"
            f"Oracle output:\n{oracle_out}\n"
            f"Agent output:\n{agent_out}\n"
        )