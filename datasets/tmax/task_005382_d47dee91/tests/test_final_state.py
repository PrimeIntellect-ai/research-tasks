# test_final_state.py

import os
import random
import string
import subprocess
import socket
import pytest

def generate_fuzz_input():
    length = random.randint(50, 200)
    prefixes = [
        "Jan 01 12:34:56 host process[123]: ",
        "2023-10-12T15:20:30Z host process: ",
        "Invalid timestamp host: ",
        "Dec 32 25:61:99 host app: ",
        ""
    ]
    prefix = random.choice(prefixes)
    charset = string.ascii_letters + string.digits + string.punctuation + " "
    body_length = max(0, length - len(prefix))
    body = "".join(random.choices(charset, k=body_length))
    return prefix + body

def test_fuzz_equivalence():
    oracle = "/app/legacy_filter.sh"
    agent = "/home/user/new_filter"

    assert os.path.exists(agent), f"Agent program {agent} does not exist."
    assert os.access(agent, os.X_OK), f"Agent program {agent} is not executable."

    random.seed(42)

    for i in range(1000):
        inp = generate_fuzz_input()

        oracle_proc = subprocess.run([oracle], input=inp, text=True, capture_output=True)
        agent_proc = subprocess.run([agent], input=inp, text=True, capture_output=True)

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Mismatch on input {i}:\n"
                f"Input: {repr(inp)}\n"
                f"Oracle output: {repr(oracle_proc.stdout)}\n"
                f"Agent output: {repr(agent_proc.stdout)}"
            )

def test_systemd_service_updated():
    path = "/home/user/.config/systemd/user/log-filter.service"
    assert os.path.exists(path), f"Service file {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "/home/user/new_filter" in content, "The systemd service ExecStart was not updated to use /home/user/new_filter."

def test_ssh_tunnel_active():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex(("127.0.0.1", 9999))
        assert result == 0, "Port 9999 is not open. The SSH tunnel to Redis is likely not active."