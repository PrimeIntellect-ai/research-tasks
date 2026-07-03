# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_libsodium_installed():
    """Verify that libsodium was built and installed locally."""
    lib_dir = "/home/user/local_libsodium/lib"
    assert os.path.isdir(lib_dir), f"Local libsodium lib directory not found at {lib_dir}"

    has_a = os.path.exists(os.path.join(lib_dir, "libsodium.a"))
    has_so = os.path.exists(os.path.join(lib_dir, "libsodium.so"))
    assert has_a or has_so, "Neither libsodium.a nor libsodium.so found in /home/user/local_libsodium/lib"

def test_decryptor_binary_exists():
    """Verify that the agent's decryptor binary exists and is executable."""
    agent_bin = "/home/user/decryptor"
    assert os.path.exists(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.path.isfile(agent_bin), f"{agent_bin} is not a file"
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable"

def generate_hex_string(length):
    return ''.join(random.choices(string.hexdigits.upper(), k=length))

def test_fuzz_equivalence():
    """Fuzz the agent's decryptor against the oracle binary."""
    oracle_bin = "/app/oracle_bin"
    agent_bin = "/home/user/decryptor"

    assert os.path.exists(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    random.seed(42)
    num_iterations = 1000

    for i in range(num_iterations):
        # argv[1] length between 64 and 256, must be even
        len_hex = random.randint(32, 128) * 2
        argv1 = generate_hex_string(len_hex)
        argv2 = generate_hex_string(4)

        args = [argv1, argv2]

        oracle_proc = subprocess.run(
            [oracle_bin] + args,
            capture_output=True,
            text=True
        )

        agent_proc = subprocess.run(
            [agent_bin] + args,
            capture_output=True,
            text=True
        )

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Return code mismatch on iteration {i}.\n"
            f"Input: {args}\n"
            f"Oracle return code: {oracle_proc.returncode}\n"
            f"Agent return code: {agent_proc.returncode}"
        )

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Stdout mismatch on iteration {i}.\n"
            f"Input: {args}\n"
            f"Oracle stdout: {repr(oracle_proc.stdout)}\n"
            f"Agent stdout: {repr(agent_proc.stdout)}"
        )

        assert oracle_proc.stderr == agent_proc.stderr, (
            f"Stderr mismatch on iteration {i}.\n"
            f"Input: {args}\n"
            f"Oracle stderr: {repr(oracle_proc.stderr)}\n"
            f"Agent stderr: {repr(agent_proc.stderr)}"
        )