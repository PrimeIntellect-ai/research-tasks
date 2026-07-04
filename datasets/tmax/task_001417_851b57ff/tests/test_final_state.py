# test_final_state.py

import os
import random
import subprocess
import tempfile
import pytest

def test_agent_executable_exists():
    assert os.path.isfile("/home/user/log_parser"), "The executable /home/user/log_parser is missing."
    assert os.access("/home/user/log_parser", os.X_OK), "/home/user/log_parser is not executable."

def test_source_code_exists_and_uses_mmap():
    assert os.path.isfile("/home/user/log_parser.c"), "The source file /home/user/log_parser.c is missing."
    with open("/home/user/log_parser.c", "r") as f:
        content = f.read()
    assert "mmap" in content, "The source code does not appear to use mmap as required."

def generate_random_input(length):
    if length == 0:
        return b""

    # Generate random bytes
    data = bytearray(os.urandom(length))

    # Inject delimiter 0xF00DBB11 with some probability
    delimiter = b"\xF0\x0D\xBB\x11"

    # To avoid making it too slow, we inject a few times randomly
    num_injections = length // 1000
    for _ in range(num_injections):
        if length >= 4:
            idx = random.randint(0, length - 4)
            data[idx:idx+4] = delimiter

    return bytes(data)

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_parser"
    agent_path = "/home/user/log_parser"

    assert os.path.isfile(oracle_path), "Oracle parser missing."

    # Edge cases
    edge_cases = [
        b"",
        b"\xF0\x0D\xBB\x11",
        b"\xF0\x0D\xBB\x11\xF0\x0D\xBB\x11",
        b"A" * 100,
        b"A" * 10 + b"\xF0\x0D\xBB\x11" + b"B" * 10,
        b"\xF0\x0D\xBB\x11" + b"A" * 10,
        b"A" * 10 + b"\xF0\x0D\xBB\x11",
    ]

    random.seed(42)
    for _ in range(50):
        length = random.randint(10, 50000)
        edge_cases.append(generate_random_input(length))

    for i, data in enumerate(edge_cases):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        try:
            oracle_proc = subprocess.run([oracle_path, tmp_path], capture_output=True)
            agent_proc = subprocess.run([agent_path, tmp_path], capture_output=True)

            assert oracle_proc.returncode == agent_proc.returncode, f"Return code mismatch on test case {i}"
            assert oracle_proc.stdout == agent_proc.stdout, f"Output mismatch on test case {i}. Length of input: {len(data)}"
            assert oracle_proc.stderr == agent_proc.stderr, f"Stderr mismatch on test case {i}"
        finally:
            os.remove(tmp_path)