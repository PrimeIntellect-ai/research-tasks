# test_final_state.py

import os
import subprocess
import stat
import random
import base64
import pytest

def test_stage1_goblin_builds():
    """Verify that the vendored goblin crate compiles successfully."""
    goblin_dir = "/app/goblin-0.7.1"
    assert os.path.isdir(goblin_dir), f"Directory {goblin_dir} does not exist"

    result = subprocess.run(
        ["cargo", "build"],
        cwd=goblin_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"cargo build failed in {goblin_dir}:\n{result.stderr.decode('utf-8', errors='replace')}"

def test_stage2_tls_certs():
    """Verify the TLS certificates and permissions."""
    cert_dir = "/home/user/certs"
    key_path = os.path.join(cert_dir, "client.key")
    crt_path = os.path.join(cert_dir, "client.crt")

    assert os.path.isfile(key_path), f"Private key missing at {key_path}"
    assert os.path.isfile(crt_path), f"Certificate missing at {crt_path}"

    # Check permissions
    st = os.stat(key_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Permissions on {key_path} are {oct(perms)}, expected 0o400"

    # Check RSA key validity
    result = subprocess.run(
        ["openssl", "rsa", "-in", key_path, "-check", "-noout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"Invalid RSA key:\n{result.stderr.decode('utf-8', errors='replace')}"

    # Check certificate validity
    result = subprocess.run(
        ["openssl", "x509", "-in", crt_path, "-noout"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"Invalid x509 certificate:\n{result.stderr.decode('utf-8', errors='replace')}"

def test_stage3_decoder_fuzz_equivalence():
    """Fuzz equivalence test for the payload decoder."""
    oracle_path = "/opt/oracle/decoder"
    agent_path = "/home/user/solution/target/release/decoder"

    assert os.path.isfile(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"

    random.seed(42)
    N = 10000

    for i in range(N):
        length = random.randint(4, 1024)
        raw_bytes = bytearray(random.getrandbits(8) for _ in range(length))

        if i % 2 == 1:
            # Valid ELF magic after XOR 0x5A
            # ELF magic: 0x7F, 0x45, 0x4C, 0x46
            raw_bytes[0] = 0x7F ^ 0x5A
            raw_bytes[1] = 0x45 ^ 0x5A
            raw_bytes[2] = 0x4C ^ 0x5A
            raw_bytes[3] = 0x46 ^ 0x5A

        b64_input = base64.b64encode(raw_bytes) + b"\n"

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=b64_input,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=b64_input,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Exit code mismatch on iteration {i}.\n"
            f"Input (base64): {b64_input.decode('utf-8').strip()}\n"
            f"Oracle exit code: {oracle_proc.returncode}\n"
            f"Agent exit code: {agent_proc.returncode}"
        )

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Stdout mismatch on iteration {i}.\n"
            f"Input (base64): {b64_input.decode('utf-8').strip()}\n"
            f"Oracle stdout length: {len(oracle_proc.stdout)}\n"
            f"Agent stdout length: {len(agent_proc.stdout)}"
        )