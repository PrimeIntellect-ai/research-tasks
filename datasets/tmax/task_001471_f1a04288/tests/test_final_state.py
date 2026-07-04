# test_final_state.py
import os
import subprocess
import time
import random
import string
import pytest

def test_nginx_gateway():
    """
    Test Objective 1: Nginx Gateway Configuration.
    Ensure Nginx is running, listening on 8443 with mTLS, and forwarding to the backend
    with the correct X-Client-CN header.
    """
    # Start services just in case they aren't running
    subprocess.run(["/app/start_services.sh"], capture_output=True)
    time.sleep(2)  # Give services a moment to start

    cmd = [
        "curl", "-s", "-k",
        "--cacert", "/app/certs/ca.crt",
        "--cert", "/app/certs/client.crt",
        "--key", "/app/certs/client.key",
        "https://127.0.0.1:8443/test"
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)

    assert res.returncode == 0, f"cURL request to gateway failed. Stderr: {res.stderr}"
    assert "OK" in res.stdout, f"Expected 'OK' from backend, but got: {res.stdout}. This indicates either proxying failed or the X-Client-CN header was not set correctly."

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_http_request():
    methods = ["GET", "POST", "PUT"]
    method = random.choice(methods)
    uri = "/" + generate_random_string(random.randint(1, 10))

    host_prefix = "internal-" if random.random() < 0.3 else ""
    host = host_prefix + generate_random_string(random.randint(5, 10))

    headers = []
    headers.append(f"Host: {host}")

    if random.random() < 0.5:
        headers.append(f"User-Agent: {generate_random_string(10)}")

    if random.random() < 0.5:
        cookie_val = "1" if random.random() < 0.5 else "0"
        cookie_name = "legacy_auth" if random.random() < 0.5 else "other_cookie"
        headers.append(f"Cookie: {cookie_name}={cookie_val}")

    req = f"{method} {uri} HTTP/1.1\r\n"
    for h in headers:
        req += f"{h}\r\n"
    req += "\r\n"

    if method in ["POST", "PUT"]:
        req += generate_random_string(random.randint(10, 50))

    return req.encode('utf-8')

def test_fuzz_equivalence():
    """
    Test Objective 2: Traffic Modification Tool.
    Fuzz equivalence verifier comparing the agent's Go program against the oracle.
    """
    oracle_path = "/app/oracle_modifier"
    agent_path = "/home/user/traffic_modifier"

    assert os.path.isfile(agent_path), f"Agent program not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program at {agent_path} is not executable"

    random.seed(42)
    n_iterations = 500

    for i in range(n_iterations):
        req_bytes = generate_http_request()

        proc_oracle = subprocess.run([oracle_path], input=req_bytes, capture_output=True)
        proc_agent = subprocess.run([agent_path], input=req_bytes, capture_output=True)

        assert proc_oracle.returncode == 0, f"Oracle failed on input: {req_bytes!r}"
        assert proc_agent.returncode == 0, f"Agent program exited with non-zero code {proc_agent.returncode} on input: {req_bytes!r}\nStderr: {proc_agent.stderr.decode('utf-8', errors='replace')}"

        if proc_oracle.stdout != proc_agent.stdout:
            error_msg = (
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input Request:\n{req_bytes!r}\n\n"
                f"Expected Output (Oracle):\n{proc_oracle.stdout!r}\n\n"
                f"Actual Output (Agent):\n{proc_agent.stdout!r}"
            )
            pytest.fail(error_msg)