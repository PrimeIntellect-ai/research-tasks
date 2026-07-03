# test_final_state.py

import os
import random
import string
import struct
import subprocess
import pytest

AGENT_BIN = "/home/user/barc2tar/target/release/barc2tar"
ORACLE_BIN = "/app/oracle_barc2tar"

def generate_valid_barc(num_entries):
    data = bytearray(b"BARC")
    data.extend(struct.pack("<I", num_entries))

    for _ in range(num_entries):
        name_len = random.randint(1, 31)
        name = "".join(random.choices(string.ascii_letters + string.digits + "._-", k=name_len)).encode("ascii")
        name_padded = name.ljust(32, b"\x00")

        file_size = random.randint(0, 10000) # smaller size to speed up tests
        file_data = bytearray(random.getrandbits(8) for _ in range(file_size))

        data.extend(name_padded)
        data.extend(struct.pack("<Q", file_size))
        data.extend(file_data)

    return bytes(data)

def generate_invalid_barc():
    kind = random.choice(["truncated_header", "bad_magic", "truncated_data", "non_ascii_name"])

    if kind == "truncated_header":
        return b"BAR"
    elif kind == "bad_magic":
        data = bytearray(b"CRAZ")
        data.extend(struct.pack("<I", 1))
        data.extend(b"test".ljust(32, b"\x00"))
        data.extend(struct.pack("<Q", 5))
        data.extend(b"12345")
        return bytes(data)
    elif kind == "truncated_data":
        data = bytearray(b"BARC")
        data.extend(struct.pack("<I", 1))
        data.extend(b"test".ljust(32, b"\x00"))
        data.extend(struct.pack("<Q", 100))
        data.extend(b"12345") # only 5 bytes
        return bytes(data)
    elif kind == "non_ascii_name":
        data = bytearray(b"BARC")
        data.extend(struct.pack("<I", 1))
        bad_name = b"\xff\xfe\xfd\xfc".ljust(32, b"\x00")
        data.extend(bad_name)
        data.extend(struct.pack("<Q", 5))
        data.extend(b"12345")
        return bytes(data)
    return b""

def run_binary(binary_path, input_data):
    try:
        result = subprocess.run(
            [binary_path],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2.0
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return None, b"", b"Timeout"

def test_barc2tar_equivalence():
    assert os.path.isfile(AGENT_BIN), f"Agent binary not found at {AGENT_BIN}"
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary at {AGENT_BIN} is not executable"

    assert os.path.isfile(ORACLE_BIN), f"Oracle binary not found at {ORACLE_BIN}"
    assert os.access(ORACLE_BIN, os.X_OK), f"Oracle binary at {ORACLE_BIN} is not executable"

    random.seed(42)

    num_tests = 500
    for i in range(num_tests):
        if random.random() < 0.8:
            num_entries = random.randint(0, 20) # keep it small for speed
            input_data = generate_valid_barc(num_entries)
        else:
            input_data = generate_invalid_barc()

        oracle_code, oracle_out, oracle_err = run_binary(ORACLE_BIN, input_data)
        agent_code, agent_out, agent_err = run_binary(AGENT_BIN, input_data)

        assert agent_code is not None, f"Agent binary timed out on test {i}"

        assert agent_code == oracle_code, f"Exit code mismatch on test {i}: oracle={oracle_code}, agent={agent_code}"
        assert agent_out == oracle_out, f"Stdout mismatch on test {i}"

        # Check stderr presence
        oracle_has_err = len(oracle_err) > 0
        agent_has_err = len(agent_err) > 0
        assert agent_has_err == oracle_has_err, f"Stderr presence mismatch on test {i}: oracle_has_err={oracle_has_err}, agent_has_err={agent_has_err}"