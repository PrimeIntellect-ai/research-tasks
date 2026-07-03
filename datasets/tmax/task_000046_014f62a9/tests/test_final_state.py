# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/bin/oracle_decoder"
AGENT_PATH = "/home/user/pipeline_decoder.py"
LOG_PATH = "/home/user/pipeline.log"

def generate_fuzz_data(num_frames=5000, seed=42):
    random.seed(seed)
    out = bytearray()
    key = b'\xA1\xB2\xC3\xD4'

    for _ in range(num_frames):
        if random.random() < 0.15:
            magic = bytes([random.randint(0, 255), random.randint(0, 255)])
        else:
            magic = b'\xFE\xED'

        encoding = random.choice([1, 2, 3])
        length = random.randint(1, 100)

        # Generate payload
        payload_bytes = bytearray()
        for _ in range(length):
            payload_bytes.append(random.randint(32, 126))

        if encoding in [2, 3] and random.random() < 0.10:
            if len(payload_bytes) > 0:
                payload_bytes[-1] = 0xFF # Invalid for UTF-8 and Shift-JIS in this context

        encrypted = bytearray(len(payload_bytes))
        for i in range(len(payload_bytes)):
            encrypted[i] = payload_bytes[i] ^ key[i % 4]

        checksum = 0
        for b in payload_bytes:
            checksum ^= b

        if random.random() < 0.15:
            checksum = (checksum + random.randint(1, 255)) % 256

        out.extend(magic)
        out.append(encoding)
        out.extend(len(payload_bytes).to_bytes(2, 'big'))
        out.extend(encrypted)
        out.append(checksum)

    return bytes(out)

def run_target(executable, input_data):
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    try:
        proc = subprocess.run(
            [executable],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        stdout = proc.stdout
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {executable} timed out.")

    log_content = b""
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "rb") as f:
            log_content = f.read()

    return stdout, log_content

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_PATH), f"Agent script not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script {AGENT_PATH} is not executable"
    assert os.path.exists(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"

    fuzz_data = generate_fuzz_data(5000, seed=1337)

    oracle_stdout, oracle_log = run_target(ORACLE_PATH, fuzz_data)
    agent_stdout, agent_log = run_target(AGENT_PATH, fuzz_data)

    if oracle_stdout != agent_stdout:
        pytest.fail("Agent stdout does not match Oracle stdout exactly on fuzzed inputs.")

    if oracle_log != agent_log:
        pytest.fail("Agent log file contents do not match Oracle log file contents exactly on fuzzed inputs.")