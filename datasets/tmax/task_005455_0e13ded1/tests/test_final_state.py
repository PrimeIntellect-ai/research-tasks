# test_final_state.py

import os
import json
import random
import string
import base64
import subprocess
import pytest

ORACLE_PATH = "/app/backup_packer"
AGENT_PATH = "/home/user/pack_backup.sh"
NUM_TESTS = 20

def generate_random_string(min_len, max_len):
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_path():
    depth = random.randint(1, 3)
    parts = [generate_random_string(3, 10) for _ in range(depth)]
    return "/".join(parts) + ".txt"

def generate_random_payload():
    prefix = generate_random_string(5, 15)
    num_items = random.randint(1, 10)
    items = []
    for _ in range(num_items):
        content_len = random.randint(10, 1000)
        content_bytes = os.urandom(content_len)
        content_b64 = base64.b64encode(content_bytes).decode('utf-8')
        mode = random.choice(["0644", "0755", "0600", "0700", "0666"])
        items.append({
            "path": generate_random_path(),
            "content": content_b64,
            "mode": mode
        })
    return {
        "prefix": prefix,
        "items": items
    }

def test_agent_script_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent script {AGENT_PATH} does not exist. Did you create it?"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script {AGENT_PATH} is not executable. Run chmod +x on it."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle {ORACLE_PATH} missing. Environment is broken."
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle {ORACLE_PATH} not executable."

    random.seed(42)

    for i in range(NUM_TESTS):
        payload = generate_random_payload()
        payload_json = json.dumps(payload)

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=payload_json.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {payload_json}: {oracle_proc.stderr.decode()}"
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=payload_json.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if agent_proc.returncode != 0:
            pytest.fail(
                f"Agent script failed (exit code {agent_proc.returncode}) on input:\n"
                f"{payload_json}\n\n"
                f"Agent stderr:\n{agent_proc.stderr.decode('utf-8', errors='replace')}"
            )

        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on test {i+1}/{NUM_TESTS}.\n"
                f"Input payload:\n{payload_json}\n\n"
                f"Oracle output length: {len(oracle_out)}\n"
                f"Agent output length: {len(agent_out)}\n"
                f"Oracle output (first 200 bytes): {oracle_out[:200]}\n"
                f"Agent output (first 200 bytes): {agent_out[:200]}"
            )