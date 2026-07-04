# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_libhasher_built():
    so_path = "/app/c-string-hasher/libhasher.so"
    assert os.path.isfile(so_path), f"Expected shared library {so_path} to be built by make."

def test_process_py_exists():
    py_path = "/home/user/process.py"
    assert os.path.isfile(py_path), f"Expected Python wrapper {py_path} to exist."

def test_ci_yml_contents():
    yml_path = "/home/user/repo/.github/workflows/ci.yml"
    assert os.path.isfile(yml_path), f"Expected CI workflow file {yml_path} to exist."

    with open(yml_path, "r") as f:
        content = f.read()

    assert "C-Extension CI" in content, "Workflow name 'C-Extension CI' not found in ci.yml"
    assert "push" in content, "'push' trigger not found in ci.yml"
    assert "pull_request" in content, "'pull_request' trigger not found in ci.yml"
    assert "main" in content, "'main' branch not found in ci.yml"
    assert "ubuntu-latest" in content, "'ubuntu-latest' runner not found in ci.yml"
    assert "actions/checkout@v3" in content, "'actions/checkout@v3' step not found in ci.yml"
    assert "make" in content, "'make' step not found in ci.yml"
    assert 'python3 process.py "test_string"' in content or "python3 process.py 'test_string'" in content, "Test step executing process.py not found in ci.yml"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/process_oracle.py"
    agent_path = "/home/user/process.py"

    assert os.path.isfile(oracle_path), f"Oracle script {oracle_path} missing."
    assert os.path.isfile(agent_path), f"Agent script {agent_path} missing."

    random.seed(42)
    chars = string.ascii_letters + string.digits

    for _ in range(50):
        length = random.randint(10, 100)
        fuzz_input = "".join(random.choice(chars) for _ in range(length))

        # Run oracle
        oracle_cmd = ["python3", oracle_path, fuzz_input]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {fuzz_input}\nStderr: {oracle_res.stderr}"
        oracle_output = oracle_res.stdout.strip()

        # Run agent
        agent_cmd = ["python3", agent_path, fuzz_input]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on input {fuzz_input}\nStderr: {agent_res.stderr}"
        agent_output = agent_res.stdout.strip()

        assert agent_output == oracle_output, (
            f"Mismatch on input: {fuzz_input}\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )