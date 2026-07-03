# test_final_state.py

import os
import random
import subprocess
import pytest

def test_cipher_fuzz_equivalence():
    oracle_path = "/app/bin/cipher_oracle"
    agent_path = "/home/user/cipher"

    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary {agent_path} is not executable"

    random.seed(42)
    N = 500
    for i in range(N):
        length = random.randint(0, 65536)
        input_data = random.randbytes(length)

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on input length {length}"
        if agent_proc.stdout != oracle_proc.stdout:
            pytest.fail(f"Output mismatch on input length {length}. Agent output did not match oracle output.")

def test_route_command():
    path = "/home/user/route_command.txt"
    assert os.path.exists(path), f"File {path} not found. The script was supposed to create it."
    with open(path, "r") as f:
        content = f.read().strip()

    expected_prefix = "ip route add 10.99.0.0/16 via 192.168.50.20"
    assert content.startswith(expected_prefix), f"Incorrect route command. Expected it to start with '{expected_prefix}', but got: {content}"

def test_setup_restore_executable():
    path = "/home/user/setup_restore.sh"
    assert os.path.exists(path), f"File {path} not found."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_restored_tar():
    tar_path = "/home/user/restored.tar"
    payload_path = "/app/backup_payload.dat"
    oracle_path = "/app/bin/cipher_oracle"

    assert os.path.exists(tar_path), f"File {tar_path} not found. The restore script may not have run successfully."

    with open(payload_path, "rb") as f:
        payload_data = f.read()

    oracle_proc = subprocess.run([oracle_path], input=payload_data, capture_output=True)
    expected_data = oracle_proc.stdout

    with open(tar_path, "rb") as f:
        actual_data = f.read()

    assert actual_data == expected_data, "Restored tar file contents do not match the expected unobfuscated data."