# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def test_clean_bin_exists_and_executable():
    path = "/home/user/clean_bin"
    assert os.path.exists(path), f"Missing file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_fuzz_equivalence():
    agent_bin = "/home/user/clean_bin"
    oracle_bin = "/app/oracle_bin"

    assert os.path.exists(oracle_bin), f"Missing oracle binary: {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary is not executable: {oracle_bin}"

    random.seed(42)
    charset = string.ascii_letters + string.digits + string.punctuation + " "

    for i in range(500):
        length = random.randint(1, 100)
        input_str = "".join(random.choices(charset, k=length))
        input_bytes = (input_str + "\n").encode('utf-8')

        try:
            oracle_proc = subprocess.run(
                [oracle_bin],
                input=input_bytes,
                capture_output=True,
                timeout=2,
                check=True
            )
            oracle_out = oracle_proc.stdout.decode('utf-8').strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle binary timed out on input: {repr(input_str)}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle binary failed with exit code {e.returncode} on input: {repr(input_str)}")

        try:
            agent_proc = subprocess.run(
                [agent_bin],
                input=input_bytes,
                capture_output=True,
                timeout=2
            )
            agent_out = agent_proc.stdout.decode('utf-8').strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on input: {repr(input_str)}")
        except Exception as e:
            pytest.fail(f"Agent binary execution failed: {e}")

        assert agent_proc.returncode == 0, f"Agent binary failed with exit code {agent_proc.returncode} on input: {repr(input_str)}\nStderr: {agent_proc.stderr.decode('utf-8', errors='ignore')}"

        assert agent_out == oracle_out, (
            f"Mismatch on input: {repr(input_str)}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent):       {agent_out}"
        )