# test_final_state.py

import os
import random
import string
import struct
import subprocess
import zlib
import pytest

ORACLE = "/app/bin/legacy_parser"
AGENT = "/home/user/new_parser"
SCHEMA_FILE = "/tmp/fuzz_schema.conf"
ARF_FILE = "/tmp/fuzz_input.arf"

def generate_schema():
    with open(SCHEMA_FILE, "w") as f:
        for i in range(256):
            if random.random() < 0.3:
                name = "".join(random.choices(string.ascii_uppercase + "_", k=random.randint(3, 15)))
                f.write(f"{i:02X}:{name}\n")
            elif random.random() < 0.05:
                # Invalid lines to ensure they are ignored
                f.write("INVALID_LINE_FORMAT\n")

def generate_arf():
    magic = b"ARF1"
    if random.random() < 0.1:
        magic = b"BADM" # invalid magic

    tlv_data = b""
    if random.random() < 0.8:
        for _ in range(random.randint(1, 20)):
            t = random.randint(0, 255)
            length = random.randint(0, 50)
            val = os.urandom(length)
            tlv_data += struct.pack("<BH", t, length)
            if random.random() < 0.05:
                # truncate TLV
                tlv_data += val[:length // 2]
                break
            else:
                tlv_data += val

    uncompressed_size = len(tlv_data)
    if random.random() < 0.1:
        uncompressed_size += random.choice([-1, 1, 5]) # invalid size

    compressed = zlib.compress(tlv_data)
    if random.random() < 0.1:
        # corrupt zlib stream
        compressed = compressed[:-5] + b"JUNK"

    with open(ARF_FILE, "wb") as f:
        f.write(magic)
        f.write(struct.pack("<I", uncompressed_size & 0xFFFFFFFF))
        f.write(compressed)
        if random.random() < 0.05:
            # truncate file
            f.truncate(random.randint(0, max(0, f.tell() - 2)))

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE), f"Oracle binary missing at {ORACLE}"
    assert os.path.isfile(AGENT), f"Agent binary missing at {AGENT}"
    assert os.access(AGENT, os.X_OK), f"Agent binary at {AGENT} is not executable"

    random.seed(1337)
    generate_schema()

    for i in range(5000):
        generate_arf()

        oracle_proc = subprocess.run([ORACLE, SCHEMA_FILE, ARF_FILE], capture_output=True)
        agent_proc = subprocess.run([AGENT, SCHEMA_FILE, ARF_FILE], capture_output=True)

        if oracle_proc.returncode != agent_proc.returncode or oracle_proc.stdout != agent_proc.stdout:
            with open(ARF_FILE, "rb") as f:
                input_data = f.read()
            pytest.fail(
                f"Mismatch on iteration {i}!\n\n"
                f"Input ARF (hex): {input_data.hex()}\n\n"
                f"Oracle exit code: {oracle_proc.returncode}\n"
                f"Agent exit code: {agent_proc.returncode}\n\n"
                f"Oracle stdout: {oracle_proc.stdout!r}\n"
                f"Agent stdout: {agent_proc.stdout!r}\n"
            )