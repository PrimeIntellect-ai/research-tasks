# test_final_state.py
import os
import subprocess
import random
import pytest

def test_fixed_seq_exists_and_executable():
    path = "/home/user/fixed_seq"
    assert os.path.isfile(path), f"Missing fixed binary: {path}"
    assert os.access(path, os.X_OK), f"Fixed binary is not executable: {path}"

def test_conf_file_exists():
    path = "/etc/math_seq.conf"
    assert os.path.isfile(path), f"Missing configuration file: {path}. Did you check the strace log?"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_seq"
    agent_path = "/home/user/fixed_seq"

    assert os.path.isfile(oracle_path), f"Missing oracle binary: {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle binary is not executable: {oracle_path}"

    random.seed(42)
    for _ in range(100):
        start_index = random.randint(1, 500)
        length = random.randint(5, 50)

        args = [str(start_index), str(length)]

        try:
            oracle_res = subprocess.run(
                [oracle_path] + args, 
                capture_output=True, 
                text=True, 
                check=True
            )
            oracle_out = oracle_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {args}. Stderr: {e.stderr}")

        try:
            agent_res = subprocess.run(
                [agent_path] + args, 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            agent_out = agent_res.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input {args}")

        if agent_res.returncode != 0:
            pytest.fail(
                f"Agent program failed with return code {agent_res.returncode} on input {args}.\n"
                f"Stderr: {agent_res.stderr}"
            )

        assert agent_out == oracle_out, (
            f"Output mismatch on input start_index={start_index}, length={length}.\n"
            f"Expected output:\n{oracle_out}\n"
            f"Actual output:\n{agent_out}"
        )