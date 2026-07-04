# test_final_state.py

import os
import random
import string
import subprocess
import zlib
import struct
import tempfile
import pytest

ORACLE_PATH = "/app/dataset_normalizer"
AGENT_PATH = "/home/user/normalizer"

def generate_random_text():
    length = random.randint(10, 500)
    chars = string.ascii_letters + string.digits + " \t"
    text = "".join(random.choice(chars) for _ in range(length))

    # Inject MISSING and \r\n
    num_missing = random.randint(0, 5)
    for _ in range(num_missing):
        pos = random.randint(0, len(text))
        text = text[:pos] + "MISSING" + text[pos:]

    num_rn = random.randint(0, 5)
    for _ in range(num_rn):
        pos = random.randint(0, len(text))
        text = text[:pos] + "\r\n" + text[pos:]

    return text.encode('utf-8')

def generate_archive(path):
    with open(path, 'wb') as f:
        f.write(b"RSRCH")
        num_chunks = random.randint(1, 10)
        f.write(bytes([num_chunks]))

        for _ in range(num_chunks):
            uncompressed_data = generate_random_text()
            compressed_data = zlib.compress(uncompressed_data)

            f.write(struct.pack("<I", len(uncompressed_data)))
            f.write(struct.pack("<I", len(compressed_data)))
            f.write(compressed_data)

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary {AGENT_PATH} not found."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    random.seed(42)

    for i in range(100):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_archive = os.path.join(tmpdir, "input.rsrch")
            generate_archive(input_archive)

            oracle_output = os.path.join(tmpdir, "oracle_out.txt")
            agent_output = os.path.join(tmpdir, "agent_out.txt")

            oracle_proc = subprocess.run([ORACLE_PATH, input_archive, oracle_output], capture_output=True)
            assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"

            agent_proc = subprocess.run([AGENT_PATH, input_archive, agent_output], capture_output=True)
            assert agent_proc.returncode == 0, f"Agent failed on input {i}. Stderr: {agent_proc.stderr.decode('utf-8', errors='ignore')}"

            assert os.path.exists(oracle_output), f"Oracle did not produce output for input {i}"
            assert os.path.exists(agent_output), f"Agent did not produce output for input {i}"

            with open(oracle_output, 'rb') as f:
                oracle_data = f.read()
            with open(agent_output, 'rb') as f:
                agent_data = f.read()

            assert oracle_data == agent_data, f"Output mismatch on input {i}. Agent output does not match oracle."

def test_atomic_rename_behavior():
    random.seed(99)
    with tempfile.TemporaryDirectory() as tmpdir:
        input_archive = os.path.join(tmpdir, "input.rsrch")
        generate_archive(input_archive)
        agent_output = os.path.join(tmpdir, "agent_out.txt")

        # Use strace to trace file operations
        strace_proc = subprocess.run(
            ["strace", "-e", "trace=rename,renameat,renameat2", AGENT_PATH, input_archive, agent_output],
            capture_output=True, text=True
        )

        assert strace_proc.returncode == 0, "Agent failed during strace."

        # Check if rename happened involving the .tmp file
        stderr = strace_proc.stderr
        expected_tmp = agent_output + ".tmp"

        assert expected_tmp in stderr and agent_output in stderr, \
            "Could not find atomic rename from .tmp to final output file in strace output."