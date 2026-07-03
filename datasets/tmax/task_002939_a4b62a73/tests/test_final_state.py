# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

def test_video_count():
    path = "/home/user/video_count.txt"
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "47", f"Expected video_count.txt to contain '47', but got '{content}'."

def test_legacy_parser_makefile_fixed():
    path = "/home/user/legacy_parser/Makefile"
    assert os.path.isfile(path), f"Makefile {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "\t" in content, "Makefile was not fixed to use tabs."

def test_legacy_parser_compiled():
    path = "/home/user/legacy_parser/payload_parser"
    assert os.path.isfile(path), f"Compiled binary {path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def encode_varint(n):
    res = []
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            res.append(b | 0x80)
        else:
            res.append(b)
            break
    return bytes(res)

def encode_string(tag, s):
    b = s.encode('utf-8')
    return encode_varint((tag << 3) | 2) + encode_varint(len(b)) + b

def encode_bytes(tag, b):
    return encode_varint((tag << 3) | 2) + encode_varint(len(b)) + b

def encode_int32(tag, n):
    if n < 0:
        n += (1 << 64)
    return encode_varint((tag << 3) | 0) + encode_varint(n)

def make_api_request(endpoint, raw_payload, timestamp):
    res = b""
    if endpoint:
        res += encode_string(1, endpoint)
    if raw_payload:
        res += encode_bytes(2, raw_payload)
    if timestamp:
        res += encode_int32(3, timestamp)
    return res

def test_fuzz_equivalence_python_parser():
    python_script = "/home/user/python_parser.py"
    oracle_bin = "/app/reference_parser"

    assert os.path.isfile(python_script), f"Python script {python_script} is missing."
    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} is missing."

    random.seed(42)
    N = 500

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(N):
            payload_len = random.randint(0, 2048)
            raw_payload = bytes(random.getrandbits(8) for _ in range(payload_len))
            endpoint = f"/api/v1/resource/{random.randint(1, 1000)}"
            timestamp = random.randint(1600000000, 1700000000)

            pb_data = make_api_request(endpoint, raw_payload, timestamp)

            input_file = os.path.join(tmpdir, f"input_{i}.bin")
            with open(input_file, "wb") as f:
                f.write(pb_data)

            # Run oracle
            oracle_proc = subprocess.run([oracle_bin, input_file], capture_output=True, text=True)
            oracle_out = oracle_proc.stdout.strip()

            # Run agent script
            agent_proc = subprocess.run(["python3", python_script, input_file], capture_output=True, text=True)
            agent_out = agent_proc.stdout.strip()

            assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on input {i} (len={payload_len}). Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}\nAgent stderr: {agent_proc.stderr}"
            assert agent_out == oracle_out, f"Output mismatch on input {i} (len={payload_len}).\nOracle: {oracle_out}\nAgent: {agent_out}"