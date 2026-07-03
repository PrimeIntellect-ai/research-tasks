# test_final_state.py
import os
import random
import string
import subprocess
import urllib.request
import urllib.error
import pytest

ORACLE_PATH = "/app/email_router_oracle"
AGENT_PATH = "/home/user/email_router"
SCRIPT_PATH = "/home/user/start_backend.sh"

def generate_fuzz_inputs(n=1000, seed=42):
    random.seed(seed)
    inputs = []
    keywords = ["Subject: URGENT", "To: dev@", "From: spammer@"]
    for _ in range(n):
        length = random.randint(10, 500)
        # Generate random printable ASCII
        chars = string.ascii_letters + string.digits + string.punctuation + " \n\t"
        base_str = "".join(random.choice(chars) for _ in range(length))

        # Randomly inject keywords to ensure different branches are hit
        if random.random() < 0.5:
            kw = random.choice(keywords)
            insert_pos = random.randint(0, len(base_str))
            base_str = base_str[:insert_pos] + kw + base_str[insert_pos:]

        # Truncate if it exceeds 500 (though slightly exceeding is fine for fuzzing)
        inputs.append(base_str[:500].encode('utf-8'))
    return inputs

def run_binary(binary_path, input_bytes):
    try:
        result = subprocess.run(
            [binary_path],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return b"<TIMEOUT>"
    except Exception as e:
        return f"<ERROR: {e}>".encode('utf-8')

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"

    inputs = generate_fuzz_inputs(1000)
    for i, inp in enumerate(inputs):
        oracle_out = run_binary(ORACLE_PATH, inp)
        agent_out = run_binary(AGENT_PATH, inp)

        assert oracle_out == agent_out, (
            f"Mismatch on input {i}:\n"
            f"Input: {inp!r}\n"
            f"Oracle output: {oracle_out!r}\n"
            f"Agent output: {agent_out!r}"
        )

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Backend script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Backend script at {SCRIPT_PATH} is not executable"

def test_nginx_routing_fixed():
    url = "http://127.0.0.1:8080/route"
    payload = b"From: someuser@example.com\nTo: dev@example.com\nSubject: Hello\n\nBody text"

    try:
        req = urllib.request.Request(url, method="POST", data=payload)
        with urllib.request.urlopen(req, timeout=3) as response:
            status = response.getcode()
            body = response.read()

            assert status == 200, f"Expected HTTP 200, got {status}"
            assert b"dev-list" in body, f"Expected 'dev-list' in response, got {body!r}"
    except urllib.error.HTTPError as e:
        assert False, f"HTTP request failed with status {e.code}: {e.read()!r}"
    except Exception as e:
        assert False, f"Failed to connect to Nginx or backend: {e}"