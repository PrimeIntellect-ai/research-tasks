# test_final_state.py

import os
import re
import socket
import subprocess
import random
import pytest

def test_nginx_config():
    config_path = "/home/user/nginx_alert.conf"
    assert os.path.isfile(config_path), f"Nginx config not found at {config_path}"
    with open(config_path, "r") as f:
        content = f.read()

    # Check for proxy_pass directive pointing to 127.0.0.1:3000
    assert re.search(r"proxy_pass\s+http://127\.0\.0\.1:3000/?;", content), "proxy_pass directive pointing to http://127.0.0.1:3000 not found in config"

def test_nginx_listening():
    # Check if a process is listening on 127.0.0.1:8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8080))
    sock.close()
    assert result == 0, "Nothing is listening on 127.0.0.1:8080"

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_alerter"
    agent_script = "/home/user/alerter.py"

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"

    random.seed(42)
    N = 5000

    for _ in range(N):
        args = [str(random.randint(0, 100)) for _ in range(5)]

        oracle_cmd = [oracle_path] + args
        agent_cmd = ["python3", agent_script] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input: {' '.join(args)}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input: {' '.join(args)}\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output: '{agent_out}'"
        )