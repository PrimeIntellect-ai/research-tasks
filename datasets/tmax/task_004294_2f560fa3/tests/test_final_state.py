# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/log_obfuscator"
    agent_path = "/home/user/obfuscator_clone"

    assert os.path.isfile(oracle_path), f"Oracle missing: {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle not executable: {oracle_path}"

    assert os.path.isfile(agent_path), f"Agent binary missing: {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary not executable: {agent_path}"

    random.seed(42)
    charset = string.printable

    # Run 1000 iterations to avoid test timeout while still providing robust fuzzing
    N = 1000
    for _ in range(N):
        length = random.randint(1, 1024)
        input_data = "".join(random.choice(charset) for _ in range(length)).encode('utf-8')

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {input_data!r}"
        assert agent_proc.returncode == 0, f"Agent failed on input: {input_data!r}"

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Mismatch found!\n"
                f"Input (hex): {input_data.hex()}\n"
                f"Oracle output (hex): {oracle_proc.stdout.hex()}\n"
                f"Agent output (hex): {agent_proc.stdout.hex()}"
            )

def test_hardened_sshd_config():
    path = "/home/user/hardened_sshd_config"
    assert os.path.isfile(path), f"Missing hardened config: {path}"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

    content = " ".join(lines)

    assert "PermitRootLogin no" in content or "permitrootlogin no" in content.lower(), "PermitRootLogin no is missing or commented out"
    assert "PermitEmptyPasswords no" in content or "permitemptypasswords no" in content.lower(), "PermitEmptyPasswords no is missing or commented out"

    # Protocol 2 is default in modern SSH, so it can be present or Protocol 1 must be absent
    assert "Protocol 1" not in content and "protocol 1" not in content.lower(), "Protocol 1 must be disabled"

    # Check MACs
    assert "MACs hmac-sha2-512,hmac-sha2-256" in content or "macs hmac-sha2-512,hmac-sha2-256" in content.lower(), "MACs are not correctly restricted to hmac-sha2-512,hmac-sha2-256"