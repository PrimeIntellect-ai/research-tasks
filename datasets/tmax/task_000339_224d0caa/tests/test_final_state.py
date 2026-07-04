# test_final_state.py

import os
import subprocess
import random
import re
import pytest

def test_bad_commit_txt():
    path = "/home/user/bad_commit.txt"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert re.match(r"^[0-9a-f]{40}$", content), f"File {path} does not contain a valid 40-character Git SHA. Found: {content}"

def test_steg_decoder_fixed_exists():
    path = "/home/user/steg_decoder_fixed"
    assert os.path.isfile(path), f"Missing executable: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/steg_decoder_golden"
    agent_path = "/home/user/steg_decoder_fixed"

    assert os.path.isfile(oracle_path), f"Oracle missing: {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent executable missing: {agent_path}"

    random.seed(42)
    n_iterations = 1000
    length = 2048

    for i in range(n_iterations):
        # Generate random binary payload
        payload = bytes(random.getrandbits(8) for _ in range(length))

        payload_path = f"/tmp/fuzz_payload_{i}.bin"
        with open(payload_path, "wb") as f:
            f.write(payload)

        try:
            oracle_proc = subprocess.run([oracle_path, payload_path], capture_output=True, timeout=5)
            agent_proc = subprocess.run([agent_path, payload_path], capture_output=True, timeout=5)

            assert oracle_proc.returncode == agent_proc.returncode, (
                f"Return code mismatch on iteration {i}.\n"
                f"Oracle: {oracle_proc.returncode}\n"
                f"Agent: {agent_proc.returncode}"
            )
            assert oracle_proc.stdout == agent_proc.stdout, (
                f"Stdout mismatch on iteration {i}.\n"
                f"Oracle stdout: {oracle_proc.stdout!r}\n"
                f"Agent stdout: {agent_proc.stdout!r}"
            )
            assert oracle_proc.stderr == agent_proc.stderr, (
                f"Stderr mismatch on iteration {i}.\n"
                f"Oracle stderr: {oracle_proc.stderr!r}\n"
                f"Agent stderr: {agent_proc.stderr!r}"
            )
        finally:
            if os.path.exists(payload_path):
                os.remove(payload_path)