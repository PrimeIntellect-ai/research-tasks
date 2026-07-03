# test_final_state.py

import os
import random
import subprocess
import json
import struct
import tempfile
import pytest

ORACLE_PATH = "/opt/oracle/abc_parser_oracle"
AGENT_PATH = "/app/abc_parser"

def generate_fuzz_inputs(seed=42, n=1000):
    random.seed(seed)
    inputs = []

    for _ in range(n):
        choice = random.random()
        if choice < 0.2:
            # 20% completely random bytes
            length = random.randint(0, 5000)
            data = bytes(random.getrandbits(8) for _ in range(length))
            inputs.append(data)
        elif choice < 0.4:
            # 20% valid magic but truncated headers
            magic = b"ARTF"
            # truncated header is anything less than 12 bytes
            length = random.randint(0, 11)
            # fill the rest with random
            rest = bytes(random.getrandbits(8) for _ in range(length))
            data = (magic + rest)[:length]
            if length >= 4:
                data = magic + rest[:length-4]
            inputs.append(data)
        else:
            # 60% valid headers
            magic = b"ARTF"
            version = 1
            flags = random.choice([0, 1])

            # Metadata
            meta_len = random.randint(0, 1000)
            meta_str = ""
            while len(meta_str) < meta_len:
                k = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=random.randint(1, 10)))
                v = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=random.randint(1, 10)))
                pair = f"{k}:{v};"
                if random.random() < 0.1:
                    pair = pair.replace(";", "") # missing semicolon
                if random.random() < 0.1:
                    pair = pair.replace(":", "::") # multiple colons
                meta_str += pair

            meta_bytes = meta_str.encode('utf-8')[:meta_len]
            actual_meta_len = len(meta_bytes)

            # Payload
            payload_len = random.randint(0, 100000)
            payload_bytes = bytes(random.getrandbits(8) for _ in range(payload_len))

            header = struct.pack("<4sBBHL", magic, version, flags, actual_meta_len, payload_len)

            # Maybe truncate the file randomly
            data = header + meta_bytes + payload_bytes
            if random.random() < 0.1:
                data = data[:random.randint(0, len(data))]

            inputs.append(data)

    return inputs

def test_cjson_fixed():
    path = "/app/cJSON/cJSON.c"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "#include <stdio_broken.h>" not in content, "cJSON.c still contains the broken include."
    assert os.path.isfile("/app/cJSON/libcjson.so"), "libcjson.so was not built."

def test_abc_parser_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent binary {AGENT_PATH} does not exist."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} missing."
    assert os.path.isfile(AGENT_PATH), f"Agent binary {AGENT_PATH} missing."

    inputs = generate_fuzz_inputs(seed=1337, n=1000)

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_name = tmp.name

    try:
        for i, data in enumerate(inputs):
            with open(tmp_name, "wb") as f:
                f.write(data)

            oracle_proc = subprocess.run([ORACLE_PATH, tmp_name], capture_output=True, text=True)
            agent_proc = subprocess.run([AGENT_PATH, tmp_name], capture_output=True, text=True)

            assert agent_proc.returncode == oracle_proc.returncode, \
                f"Exit code mismatch on input {i} (len {len(data)}).\nOracle: {oracle_proc.returncode}\nAgent: {agent_proc.returncode}"

            if oracle_proc.stdout.strip():
                try:
                    oracle_json = json.loads(oracle_proc.stdout)
                except json.JSONDecodeError:
                    oracle_json = oracle_proc.stdout.strip()
            else:
                oracle_json = None

            if agent_proc.stdout.strip():
                try:
                    agent_json = json.loads(agent_proc.stdout)
                except json.JSONDecodeError:
                    agent_json = agent_proc.stdout.strip()
            else:
                agent_json = None

            assert agent_json == oracle_json, \
                f"Stdout mismatch on input {i} (len {len(data)}).\nOracle: {oracle_json}\nAgent: {agent_json}"

    finally:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)