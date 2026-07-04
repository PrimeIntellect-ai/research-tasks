# test_final_state.py

import os
import random
import subprocess
import tempfile
import pytest

def test_weights_cfg_recovered():
    filepath = "/app/weights.cfg"
    assert os.path.isfile(filepath), f"File {filepath} was not recovered."
    with open(filepath, "r") as f:
        content = f.read().strip()
    expected_content = "0.5 1.2 3.14159"
    assert content == expected_content, f"Content of {filepath} is incorrect. Expected '{expected_content}', got '{content}'."

def test_libmatrix_compiled():
    executable_path = "/app/libmatrix-0.9/libmatrix"
    assert os.path.isfile(executable_path), f"Executable {executable_path} was not compiled."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_process_logs_fuzz_equivalence():
    oracle_path = "/opt/oracle/process_logs_oracle.sh"
    agent_path = "/app/process_logs.sh"

    assert os.path.isfile(oracle_path), f"Oracle script {oracle_path} is missing."
    assert os.path.isfile(agent_path), f"Agent script {agent_path} is missing."
    assert os.access(agent_path, os.X_OK), f"Agent script {agent_path} is not executable."

    random.seed(42)
    N = 50

    for i in range(N):
        num_lines = random.randint(10, 100)
        lines = []
        for _ in range(num_lines):
            floats = [round(random.uniform(-1000.0, 1000.0), 6) for _ in range(3)]
            lines.append(" ".join(f"{f:.6f}" for f in floats))

        input_content = "\n".join(lines) + "\n"

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write(input_content)
            tmp_path = tmp.name

        try:
            oracle_cmd = [oracle_path, tmp_path]
            agent_cmd = [agent_path, tmp_path]

            try:
                oracle_output = subprocess.check_output(oracle_cmd, text=True, timeout=10)
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Oracle failed on input {i}: {e.output}")
            except subprocess.TimeoutExpired:
                pytest.fail(f"Oracle timed out on input {i}")

            try:
                agent_output = subprocess.check_output(agent_cmd, text=True, timeout=10)
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Agent script failed on input {i} (return code {e.returncode}):\n{e.output}")
            except subprocess.TimeoutExpired:
                pytest.fail(f"Agent script timed out (deadlock?) on input {i}")

            assert agent_output == oracle_output, (
                f"Output mismatch on random input {i}.\n"
                f"Input lines: {num_lines}\n"
                f"Oracle output: {repr(oracle_output)}\n"
                f"Agent output: {repr(agent_output)}"
            )
        finally:
            os.remove(tmp_path)