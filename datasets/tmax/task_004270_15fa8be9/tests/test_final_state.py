# test_final_state.py

import os
import random
import subprocess
import re
import urllib.request
import ssl
import time
import socket

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_health_checker"
    agent_path = "/home/user/new_health_checker.py"

    assert os.path.isfile(oracle_path), f"Oracle missing: {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent script missing: {agent_path}"

    random.seed(42)
    N = 1000

    for _ in range(N):
        arg1 = random.randint(0, 1000000)
        arg2 = random.randint(arg1 + 1, 2000000)
        arg3 = random.randint(0, 128000)
        arg4 = random.randint(0, 2000)

        args = [str(arg1), str(arg2), str(arg3), str(arg4)]

        oracle_cmd = [oracle_path] + args
        agent_cmd = ["python3", agent_path] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on args {args}"
        assert agent_res.returncode == 0, f"Agent failed on args {args}"

        assert oracle_res.stdout == agent_res.stdout, \
            f"Output mismatch on args {args}.\nOracle: {oracle_res.stdout!r}\nAgent: {agent_res.stdout!r}"

def test_monitor_script_exists():
    monitor_path = "/home/user/monitor.sh"
    assert os.path.isfile(monitor_path), f"Monitor script missing: {monitor_path}"
    assert os.access(monitor_path, os.X_OK) or os.access(monitor_path, os.R_OK), \
        f"Monitor script {monitor_path} must be executable or readable."

def test_tls_certs_exist():
    cert_path = "/home/user/cert.pem"
    key_path = "/home/user/key.pem"
    assert os.path.isfile(cert_path), f"TLS cert missing: {cert_path}"
    assert os.path.isfile(key_path), f"TLS key missing: {key_path}"

def test_web_server_listening_and_response():
    # Check if port 8443 is listening
    port_open = False
    for _ in range(5):
        try:
            with socket.create_connection(("127.0.0.1", 8443), timeout=1):
                port_open = True
                break
        except OSError:
            time.sleep(1)

    assert port_open, "No process is listening on port 8443."

    # Check HTTPS response
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://127.0.0.1:8443/")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8').strip()
    except Exception as e:
        pytest.fail(f"Failed to fetch from HTTPS server: {e}")

    pattern = r"^STATUS: (OK|WARN|CRIT) - Score: \d+$"
    assert re.match(pattern, body), f"Response format invalid. Got: {body!r}"