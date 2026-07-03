# test_final_state.py

import os
import random
import subprocess
import base64
import pytest

def test_vendored_code_is_fixed():
    """Verify that the vendored openssl.go contains the restored 'Salted__' string."""
    openssl_go_path = "/app/vendor/github.com/Luzifer/go-openssl/openssl.go"
    assert os.path.exists(openssl_go_path), f"openssl.go not found at {openssl_go_path}"

    with open(openssl_go_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Salted__" in content, f"The original string ('Salted__') was not restored in {openssl_go_path}"
    assert "Hacked__" not in content, f"The perturbed string ('Hacked__') is still present in {openssl_go_path}"

def test_fuzz_equivalence():
    """Fuzz the agent's decryptor against the oracle decoder."""
    agent_bin = "/home/user/decryptor"
    oracle_bin = "/opt/oracle/decoder"

    assert os.path.exists(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"
    assert os.path.exists(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary at {oracle_bin} is not executable"

    random.seed(42)
    inputs = []

    # Generate 100 valid OpenSSL encrypted base64 strings
    for _ in range(100):
        plaintext = os.urandom(random.randint(10, 100))
        # go-openssl v2+ typically uses sha256 by default for key derivation
        proc = subprocess.run(
            ["openssl", "enc", "-aes-256-cbc", "-md", "sha256", "-pass", "pass:CSP_Secret_Key_2024", "-base64", "-A"],
            input=plaintext,
            capture_output=True
        )
        if proc.returncode == 0:
            inputs.append(proc.stdout)
        else:
            # Fallback to md5 if sha256 fails or isn't supported in this openssl version
            proc_md5 = subprocess.run(
                ["openssl", "enc", "-aes-256-cbc", "-md", "md5", "-pass", "pass:CSP_Secret_Key_2024", "-base64", "-A"],
                input=plaintext,
                capture_output=True
            )
            if proc_md5.returncode == 0:
                inputs.append(proc_md5.stdout)

    # Generate 100 random base64 strings (invalid/corrupted)
    for _ in range(100):
        length = random.randint(16, 256)
        inputs.append(base64.b64encode(os.urandom(length)))

    # Ensure we have inputs to test
    assert len(inputs) > 100, "Failed to generate test inputs."

    for i, test_input in enumerate(inputs):
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=test_input,
            capture_output=True
        )

        agent_proc = subprocess.run(
            [agent_bin],
            input=test_input,
            capture_output=True
        )

        # Compare return codes (both zero or both non-zero)
        oracle_success = (oracle_proc.returncode == 0)
        agent_success = (agent_proc.returncode == 0)

        assert oracle_success == agent_success, (
            f"Return code mismatch on input {i}. "
            f"Oracle success: {oracle_success} (code {oracle_proc.returncode}), "
            f"Agent success: {agent_success} (code {agent_proc.returncode}). "
            f"Input: {test_input[:50]}..."
        )

        # Compare stdout
        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Stdout mismatch on input {i}.\n"
            f"Oracle: {oracle_proc.stdout!r}\n"
            f"Agent:  {agent_proc.stdout!r}\n"
            f"Input: {test_input[:50]}..."
        )