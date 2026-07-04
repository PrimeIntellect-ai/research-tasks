# test_final_state.py

import os
import sys
import subprocess
import random
import string
import pytest

def xor_crypt(data: bytes, key: bytes) -> bytes:
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def generate_random_http_request(seed: int) -> bytes:
    rng = random.Random(seed)

    methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
    paths = ["/", "/login", "/api/data", "/users", "/admin/settings"]
    versions = ["HTTP/1.0", "HTTP/1.1"]

    method = rng.choice(methods)
    path = rng.choice(paths)
    version = rng.choice(versions)

    headers = {
        "Host": rng.choice(["example.com", "test.local", "api.service.io"]),
        "User-Agent": rng.choice(["curl/7.68.0", "Mozilla/5.0", "CustomApp/1.0"]),
        "Accept": "*/*"
    }

    # Generate cookies
    cookies = []
    if rng.random() > 0.1:
        for _ in range(rng.randint(0, 3)):
            name = "".join(rng.choices(string.ascii_letters, k=rng.randint(3, 8)))
            val = "".join(rng.choices(string.ascii_letters + string.digits, k=rng.randint(5, 15)))
            cookies.append(f"{name}={val}")

    # Add AuthToken
    if rng.random() > 0.1:
        # Generate payload
        payload_parts = []
        if rng.random() > 0.2:
            payload_parts.append(f"user={''.join(rng.choices(string.ascii_lowercase, k=5))}")

        if rng.random() > 0.2:
            ssn = "".join(rng.choices(string.digits, k=9))
            payload_parts.append(f"SSN={ssn}")

        if rng.random() > 0.2:
            payload_parts.append(f"role={rng.choice(['admin', 'user', 'guest'])}")

        payload_str = ";".join(payload_parts)
        if not payload_str:
            payload_str = "empty=true"

        key = b"OMEGA99"
        encrypted = xor_crypt(payload_str.encode('utf-8'), key).hex().upper()

        # Randomly corrupt the hex
        if rng.random() < 0.05:
            encrypted += "XX"

        cookies.append(f"AuthToken={encrypted}")

    rng.shuffle(cookies)
    if cookies:
        headers["Cookie"] = "; ".join(cookies)

    body = ""
    if method in ["POST", "PUT"]:
        body = "".join(rng.choices(string.ascii_letters + string.digits, k=rng.randint(10, 100)))
        headers["Content-Length"] = str(len(body))

    req_lines = [f"{method} {path} {version}"]
    for k, v in headers.items():
        req_lines.append(f"{k}: {v}")

    req_str = "\r\n".join(req_lines) + "\r\n\r\n" + body
    return req_str.encode('utf-8')

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_redactor"
    agent_script = "/home/user/redactor.py"

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"

    N = 200
    for i in range(N):
        req_bytes = generate_random_http_request(seed=42 + i)

        # Run oracle
        proc_oracle = subprocess.run(
            [oracle_path],
            input=req_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        assert proc_oracle.returncode == 0, f"Oracle failed on input {i}"

        # Run agent
        proc_agent = subprocess.run(
            [sys.executable, agent_script],
            input=req_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        if proc_agent.returncode != 0:
            pytest.fail(f"Agent script failed with return code {proc_agent.returncode} on input {i}.\nStderr: {proc_agent.stderr.decode(errors='replace')}")

        if proc_oracle.stdout != proc_agent.stdout:
            pytest.fail(
                f"Output mismatch on input {i}.\n"
                f"Input:\n{req_bytes.decode(errors='replace')}\n\n"
                f"Oracle Output:\n{proc_oracle.stdout.decode(errors='replace')}\n\n"
                f"Agent Output:\n{proc_agent.stdout.decode(errors='replace')}"
            )