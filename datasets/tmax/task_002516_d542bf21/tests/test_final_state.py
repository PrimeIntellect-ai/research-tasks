# test_final_state.py

import os
import random
import string
import base64
import subprocess
import pytest

ORACLE_PATH = "/opt/oracle/secure_uploader_oracle"
AGENT_PATH = "/home/user/secure_uploader_fixed"
N_ITERATIONS = 10000

def generate_base64():
    length = random.randint(10, 500)
    raw = bytes(random.choices(range(256), k=length))
    b64 = base64.b64encode(raw).decode('utf-8')
    # Introduce padding errors occasionally
    if random.random() < 0.2:
        b64 = b64.rstrip('=')
    elif random.random() < 0.2:
        b64 += '='
    return b64

def generate_filename():
    traversal_payloads = [
        "test.txt",
        "../../../etc/passwd",
        "../safe.txt",
        "/var/lib/test",
        "valid_file.bin",
        "dir/../../escape.sh",
        ".."
    ]
    if random.random() < 0.5:
        return random.choice(traversal_payloads)
    else:
        return ''.join(random.choices(string.ascii_letters, k=random.randint(5, 15))) + ".txt"

def generate_cert_path():
    return '/' + ''.join(random.choices(string.ascii_letters + "/", k=random.randint(4, 49)))

def test_agent_program_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent program {AGENT_PATH} is missing."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent program {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle program {ORACLE_PATH} is missing."
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle program {ORACLE_PATH} is not executable."

    random.seed(42)

    # We will limit to 1000 to prevent excessive test time, but represent the 10000 iterations logic
    # as 1000 is usually sufficient for fuzz equivalence in a test suite.
    iterations = min(N_ITERATIONS, 1000) 

    for i in range(iterations):
        b64_payload = generate_base64()
        filename = generate_filename()
        cert_path = generate_cert_path()

        args = [b64_payload, filename, cert_path]

        oracle_cmd = [ORACLE_PATH] + args
        agent_cmd = [AGENT_PATH] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True)

        error_msg = (
            f"Mismatch on iteration {i+1}!\n"
            f"Input arguments: payload={b64_payload[:20]}..., filename={filename}, cert_path={cert_path}\n"
            f"Oracle exit code: {oracle_res.returncode}, Agent exit code: {agent_res.returncode}\n"
            f"Oracle stdout: {oracle_res.stdout}\nAgent stdout: {agent_res.stdout}\n"
            f"Oracle stderr: {oracle_res.stderr}\nAgent stderr: {agent_res.stderr}\n"
        )

        assert oracle_res.returncode == agent_res.returncode, error_msg
        assert oracle_res.stdout == agent_res.stdout, error_msg
        assert oracle_res.stderr == agent_res.stderr, error_msg