# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

def test_auth_parser_tests_pass():
    """Verify that the auth_parser package tests pass after the fix."""
    work_dir = "/app/vendored/auth_parser-1.2.0"
    assert os.path.isdir(work_dir), f"Directory {work_dir} does not exist."

    result = subprocess.run(
        ["python3", "-m", "unittest", "discover"],
        cwd=work_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"Tests failed in {work_dir}. Stderr: {result.stderr}"

def test_cracked_password():
    """Verify that the cracked password file exists and contains the correct password."""
    path = "/home/user/audit_logs/cracked_pass.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert content.strip() == "apple", f"Expected cracked password 'apple', got '{content.strip()}'"

def test_evaluator_agent_fuzz():
    """Verify that the evaluator_agent is functionally equivalent to the oracle."""
    oracle_path = "/opt/oracle/perm_eval_oracle"
    agent_path = "/home/user/evaluator_agent"

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} not found."
    assert os.path.isfile(agent_path), f"Agent script {agent_path} not found."
    assert os.access(agent_path, os.X_OK), f"Agent script {agent_path} is not executable."

    N_iterations = 5000
    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        file1_path = os.path.join(tmpdir, "input1.bin")
        file2_path = os.path.join(tmpdir, "input2.bin")

        for i in range(N_iterations):
            len1 = random.randint(1, 1024)
            len2 = random.randint(1, 1024)

            data1 = bytes([random.randint(0, 255) for _ in range(len1)])
            data2 = bytes([random.randint(0, 255) for _ in range(len2)])

            with open(file1_path, "wb") as f1, open(file2_path, "wb") as f2:
                f1.write(data1)
                f2.write(data2)

            oracle_res = subprocess.run(
                [oracle_path, file1_path, file2_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            agent_res = subprocess.run(
                [agent_path, file1_path, file2_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if oracle_res.returncode != agent_res.returncode or oracle_res.stdout != agent_res.stdout:
                pytest.fail(
                    f"Mismatch on iteration {i+1}:\n"
                    f"Input 1 length: {len1}, Input 2 length: {len2}\n"
                    f"Oracle returncode: {oracle_res.returncode}, Agent returncode: {agent_res.returncode}\n"
                    f"Oracle stdout (hex): {oracle_res.stdout.hex()[:100]}...\n"
                    f"Agent stdout (hex): {agent_res.stdout.hex()[:100]}...\n"
                )