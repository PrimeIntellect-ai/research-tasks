# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_migrated_processor_cpp_exists():
    """Verify that the C++ source file was created."""
    path = "/home/user/migrated_processor.cpp"
    assert os.path.isfile(path), f"Missing C++ source file at {path}"

def test_deploy_script_exists_and_executable():
    """Verify that the deployment script exists and is executable."""
    path = "/home/user/deploy.sh"
    assert os.path.isfile(path), f"Missing deployment script at {path}"
    assert os.access(path, os.X_OK), f"Deployment script at {path} is not executable"

def test_deploy_script_contents():
    """Verify that the deployment script contains the required commands."""
    path = "/home/user/deploy.sh"
    with open(path, "r") as f:
        content = f.read()

    # Check for SSH tunnel
    assert "ssh" in content and "-L" in content and "8080:localhost:9090" in content, \
        "Deployment script does not contain the correct SSH port forwarding command."

    # Check for python http.server
    assert "python3" in content and "http.server" in content and "9090" in content, \
        "Deployment script does not contain the python http.server command."

    # Check for health log
    assert "health.log" in content, \
        "Deployment script does not write to health.log."

def test_fuzz_equivalence():
    """Fuzz test the migrated processor against the oracle binary."""
    oracle_path = "/app/oracle_bin"
    agent_path = "/home/user/migrated_processor"

    assert os.path.isfile(agent_path), f"Missing compiled binary at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Binary at {agent_path} is not executable"

    random.seed(42)
    chars = string.ascii_letters + string.digits

    for _ in range(5000):
        length = random.randint(5, 50)
        test_input = "".join(random.choices(chars, k=length))

        oracle_proc = subprocess.run([oracle_path, test_input], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_path, test_input], capture_output=True, text=True)

        assert oracle_proc.returncode == agent_proc.returncode, \
            f"Return code mismatch on input '{test_input}': oracle={oracle_proc.returncode}, agent={agent_proc.returncode}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, \
            f"Output mismatch on input '{test_input}'.\nOracle: {oracle_out}\nAgent:  {agent_out}"