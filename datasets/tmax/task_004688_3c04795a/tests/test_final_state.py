# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

ORACLE_BIN = "/app/legacy_web_scanner"
AGENT_BIN = "/home/user/new_web_scanner"
NUM_TESTS = 50

def generate_random_string(min_len=4, max_len=8):
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def setup_random_directory(base_dir):
    num_users = random.randint(0, 20)
    user_names = set()
    while len(user_names) < num_users:
        user_names.add(generate_random_string())

    for user in user_names:
        user_dir = os.path.join(base_dir, user)
        os.makedirs(user_dir)

        # 50% chance of public_html
        if random.random() < 0.5:
            os.makedirs(os.path.join(user_dir, "public_html"))

        # 50% chance of tls/cert.pem symlink
        if random.random() < 0.5:
            tls_dir = os.path.join(user_dir, "tls")
            os.makedirs(tls_dir)
            target = f"/etc/certs/{generate_random_string()}.pem"
            os.symlink(target, os.path.join(tls_dir, "cert.pem"))

def test_agent_binary_exists():
    assert os.path.exists(AGENT_BIN), f"Agent binary not found at {AGENT_BIN}"
    assert os.path.isfile(AGENT_BIN), f"{AGENT_BIN} is not a file"
    assert os.access(AGENT_BIN, os.X_OK), f"{AGENT_BIN} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BIN), f"Oracle binary not found at {ORACLE_BIN}"
    assert os.path.exists(AGENT_BIN), f"Agent binary not found at {AGENT_BIN}"

    random.seed(42)

    for i in range(NUM_TESTS):
        with tempfile.TemporaryDirectory() as temp_dir:
            setup_random_directory(temp_dir)

            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_BIN, temp_dir],
                capture_output=True,
                text=True,
                timeout=5
            )
            oracle_out = oracle_proc.stdout

            # Run agent
            agent_proc = subprocess.run(
                [AGENT_BIN, temp_dir],
                capture_output=True,
                text=True,
                timeout=5
            )
            agent_out = agent_proc.stdout

            assert agent_proc.returncode == oracle_proc.returncode, (
                f"Return code mismatch on test {i+1}/{NUM_TESTS}.\n"
                f"Input dir: {temp_dir}\n"
                f"Oracle returncode: {oracle_proc.returncode}\n"
                f"Agent returncode: {agent_proc.returncode}"
            )

            assert agent_out == oracle_out, (
                f"Output mismatch on test {i+1}/{NUM_TESTS}.\n"
                f"Input dir: {temp_dir}\n"
                f"Oracle output:\n{oracle_out}\n"
                f"Agent output:\n{agent_out}"
            )