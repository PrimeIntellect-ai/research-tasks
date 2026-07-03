# test_final_state.py
import os
import sys
import struct
import random
import string
import subprocess
import time
import pytest

ORACLE_PATH = "/opt/oracle/parse_single_oracle.py"
AGENT_PATH = "/home/user/parse_single.py"

def generate_fuzz_input(seed: int) -> bytes:
    random.seed(seed)
    length = random.randint(1024, 1024 * 100) # 1KB to 100KB for speed
    num_records = random.randint(0, 50)

    data = bytearray(os.urandom(length))

    # Insert records
    insert_positions = sorted([random.randint(0, length - 1) for _ in range(num_records)])

    # Build records
    records = []
    for _ in range(num_records):
        payload_len = random.randint(1, 1000)
        # Generate random text
        chars = string.ascii_letters + string.digits + " \n\t"
        payload = "".join(random.choices(chars, k=payload_len))

        # Randomly insert "DRAFT"
        if random.random() < 0.5:
            insert_idx = random.randint(0, len(payload))
            payload = payload[:insert_idx] + "DRAFT" + payload[insert_idx:]

        # Randomly add trailing spaces
        if random.random() < 0.5:
            payload += "   \t \n"

        payload_bytes = payload.encode('utf-8')
        record = b"DOC_BETA_99" + struct.pack("<I", len(payload_bytes)) + payload_bytes
        records.append(record)

    # Combine
    result = bytearray()
    last_pos = 0
    for pos, record in zip(insert_positions, records):
        if pos > last_pos:
            result.extend(data[last_pos:pos])
        result.extend(record)
        last_pos = pos

    if last_pos < len(data):
        result.extend(data[last_pos:])

    return bytes(result)

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent script not found at {AGENT_PATH}"

    N = 100
    for i in range(N):
        input_data = generate_fuzz_input(seed=i)

        oracle_proc = subprocess.run(
            [sys.executable, ORACLE_PATH],
            input=input_data,
            capture_output=True
        )

        agent_proc = subprocess.run(
            [sys.executable, AGENT_PATH],
            input=input_data,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed on seed {i} with stderr: {agent_proc.stderr.decode(errors='replace')}"

        oracle_out = oracle_proc.stdout
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on seed {i}.\n"
                f"Oracle output length: {len(oracle_out)}\n"
                f"Agent output length: {len(agent_out)}\n"
                f"Oracle output start: {oracle_out[:200]!r}\n"
                f"Agent output start: {agent_out[:200]!r}"
            )

def test_watcher_script_exists():
    assert os.path.exists("/home/user/watcher.py"), "watcher.py is missing"
    assert os.path.exists("/home/user/incoming"), "/home/user/incoming directory is missing"
    assert os.path.exists("/home/user/processed"), "/home/user/processed directory is missing"