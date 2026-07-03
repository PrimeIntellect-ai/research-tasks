# test_final_state.py

import os
import sys
import subprocess
import random
import string
import struct
import zlib
import shutil
import pytest
import ast

AGENT_SCRIPT = "/home/user/safe_extract.py"
ORACLE_SCRIPT = "/opt/oracle/safe_extract_oracle.py"
EXTRACT_DIR = "/home/user/extracted"
PYTHONPATH = "/app/zstream-1.2.0"

def generate_zstream(records):
    """
    Generates a binary stream compliant with the custom zstream format.
    [2 bytes filename len][filename bytes][4 bytes compressed len][zlib compressed data]
    """
    out = bytearray()
    for fname, data in records:
        comp = zlib.compress(data)
        # Using big-endian for standard network byte order, though the vendored package handles it.
        out.extend(struct.pack(">H", len(fname)))
        out.extend(fname)
        out.extend(struct.pack(">I", len(comp)))
        out.extend(comp)
    return bytes(out)

def get_random_path(basename):
    prefixes = [
        b"../",
        b"..\\",
        b"/absolute/path/",
        b"subdir/",
        b"../../etc/",
        b""
    ]
    return random.choice(prefixes) + basename

def run_script(script_path, input_data):
    env = os.environ.copy()
    env["PYTHONPATH"] = PYTHONPATH
    proc = subprocess.Popen(
        [sys.executable, script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    stdout, stderr = proc.communicate(input=input_data)
    return proc.returncode, stdout, stderr

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script missing: {AGENT_SCRIPT}"
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script missing: {ORACLE_SCRIPT}"

    # Verify fcntl.flock is used in the agent script
    with open(AGENT_SCRIPT, "r") as f:
        code = f.read()

    assert "fcntl.flock" in code, "Agent script must use fcntl.flock for concurrency safety."

    random.seed(42)
    N = 10

    # Generate common basenames to trigger write contention
    basenames = [f"file_{i}.bin".encode() for i in range(5)]

    inputs = []
    for _ in range(N):
        num_records = random.randint(2, 5)
        records = []
        for _ in range(num_records):
            basename = random.choice(basenames)
            fname = get_random_path(basename)
            data_len = random.randint(10, 500)
            data = bytes(random.getrandbits(8) for _ in range(data_len))
            records.append((fname, data))
        inputs.append(generate_zstream(records))

    # Clear extract dir
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    # Run oracle sequentially
    for input_data in inputs:
        ret, out, err = run_script(ORACLE_SCRIPT, input_data)
        assert ret == 0, f"Oracle failed with error: {err.decode()}"

    oracle_files = {}
    for root, _, files in os.walk(EXTRACT_DIR):
        for file in files:
            path = os.path.join(root, file)
            with open(path, "rb") as f:
                oracle_files[file] = f.read()

    # Clear extract dir for agent
    shutil.rmtree(EXTRACT_DIR)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    # Run agent sequentially to ensure deterministic append order for exact byte matching
    for i, input_data in enumerate(inputs):
        ret, out, err = run_script(AGENT_SCRIPT, input_data)
        assert ret == 0, f"Agent script failed on input {i} with error: {err.decode()}"

    agent_files = {}
    for root, _, files in os.walk(EXTRACT_DIR):
        for file in files:
            path = os.path.join(root, file)
            with open(path, "rb") as f:
                agent_files[file] = f.read()

    # Compare results
    assert set(agent_files.keys()) == set(oracle_files.keys()), \
        f"Extracted files mismatch. Expected {set(oracle_files.keys())}, got {set(agent_files.keys())}"

    for file in oracle_files:
        assert agent_files[file] == oracle_files[file], \
            f"Content mismatch for file {file}. Agent did not extract or append correctly."