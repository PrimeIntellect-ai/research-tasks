# test_final_state.py
import os
import json
import random
import string
import subprocess
import pytest

def test_brotli_setup_py_fixed():
    setup_path = "/app/brotli-1.1.0/setup.py"
    assert os.path.isfile(setup_path), f"{setup_path} is missing"
    with open(setup_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "extr_compile_args" not in content, "The typo 'extr_compile_args' is still present in setup.py. It should be fixed."
    assert "extra_compile_args" in content, "The correct 'extra_compile_args' is missing in setup.py."

def test_archive_py_exists():
    assert os.path.isfile("/home/user/archive.py"), "/home/user/archive.py is missing"

def test_fuzz_equivalence():
    random.seed(42)
    oracle_path = "/app/oracle_archiver"
    agent_path = "/home/user/archive.py"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"

    # Determine how to run the oracle
    if os.access(oracle_path, os.X_OK):
        oracle_cmd = [oracle_path]
    else:
        oracle_cmd = ["python3", oracle_path]

    agent_cmd = ["python3", agent_path]

    for i in range(500):
        num_lines = random.randint(10, 100)
        lines = []
        for _ in range(num_lines):
            msg_len = random.randint(10, 500)
            msg = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation + " ", k=msg_len))
            lines.append(json.dumps({"timestamp": "2023-10-01T12:00:00Z", "message": msg}))

        input_data = "\n".join(lines) + "\n"
        input_bytes = input_data.encode('utf-8')

        try:
            oracle_proc = subprocess.run(oracle_cmd, input=input_bytes, capture_output=True, check=True)
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on iteration {i}: {e.stderr.decode('utf-8', errors='replace')}")

        try:
            agent_proc = subprocess.run(agent_cmd, input=input_bytes, capture_output=True, check=True)
            agent_out = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on iteration {i}: {e.stderr.decode('utf-8', errors='replace')}")

        if agent_out != oracle_out:
            pytest.fail(
                f"Output mismatch on iteration {i}.\n"
                f"Input length: {len(input_bytes)} bytes ({num_lines} lines)\n"
                f"Oracle output length: {len(oracle_out)} bytes\n"
                f"Agent output length: {len(agent_out)} bytes\n"
                f"First line of input: {lines[0]}"
            )