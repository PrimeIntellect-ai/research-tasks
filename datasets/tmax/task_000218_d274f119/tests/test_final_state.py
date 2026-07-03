# test_final_state.py

import os
import random
import string
import subprocess
import socket
import pytest

def test_ssh_tunnel_running():
    """Verify that a local port 8080 is listening (the SSH tunnel)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        result = s.connect_ex(("127.0.0.1", 8080))
        assert result == 0, "No service listening on 127.0.0.1:8080. The SSH tunnel is missing or not running."
    finally:
        s.close()

def test_agent_program_exists():
    """Verify that the agent's compiled CLI exists and is executable."""
    agent_path = "/home/user/quota_cli"
    assert os.path.exists(agent_path), f"{agent_path} does not exist."
    assert os.path.isfile(agent_path), f"{agent_path} is not a file."
    assert os.access(agent_path, os.X_OK), f"{agent_path} is not executable."

def test_fuzz_equivalence():
    """Fuzz-test the agent's program against the oracle binary."""
    oracle_path = "/app/oracle_bin"
    agent_path = "/home/user/quota_cli"

    assert os.path.exists(oracle_path), f"Oracle binary {oracle_path} missing."
    assert os.path.exists(agent_path), f"Agent binary {agent_path} missing."

    random.seed(42)
    chars = string.ascii_lowercase + string.digits

    for _ in range(20):
        length = random.randint(4, 12)
        username = "".join(random.choices(chars, k=length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=username.encode('utf-8'),
            capture_output=True
        )
        oracle_stdout = oracle_proc.stdout.decode('utf-8')

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=username.encode('utf-8'),
            capture_output=True
        )
        agent_stdout = agent_proc.stdout.decode('utf-8')

        assert agent_stdout == oracle_stdout, (
            f"Output mismatch for input '{username}'.\n"
            f"Expected (oracle):\n{oracle_stdout}\n"
            f"Got (agent):\n{agent_stdout}\n"
        )