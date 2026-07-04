# test_final_state.py
import os
import subprocess
import random
import string
import struct
import tempfile
import pytest

ORACLE_PATH = '/app/log_parser_oracle'
AGENT_PATH = '/home/user/my_parser'

def generate_valid_record():
    record_type = random.choice([0x10, 0x11, 0x30])
    timestamp = random.randint(0, 2**64 - 1)

    if record_type == 0x10:
        payload = struct.pack('<i', random.randint(-2**31, 2**31 - 1))
    elif record_type == 0x11:
        payload = struct.pack('<q', random.randint(-2**63, 2**63 - 1))
    else:
        length = random.randint(0, 100)
        chars = string.ascii_letters + string.digits + " \n\t\\"
        payload = ''.join(random.choice(chars) for _ in range(length)).encode('ascii')

    length = len(payload)
    header = struct.pack('<B Q H', record_type, timestamp, length)

    data = header + payload
    checksum = 0
    for b in data:
        checksum ^= b

    return data + struct.pack('<B', checksum)

def generate_fuzz_input(seed):
    random.seed(seed)
    num_records = random.randint(10, 500)

    data = bytearray(b"DAT\x00")
    for _ in range(num_records):
        data.extend(generate_valid_record())

    # Mutate 1-5% of bytes, excluding the first 4 bytes
    num_mutations = int(len(data) * random.uniform(0.01, 0.05))
    for _ in range(num_mutations):
        idx = random.randint(4, len(data) - 1)
        data[idx] = random.randint(0, 255)

    return bytes(data)

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent binary missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"

    N = 100
    for i in range(N):
        input_data = generate_fuzz_input(seed=42 + i)

        with tempfile.NamedTemporaryFile(delete=False) as f_in:
            f_in.write(input_data)
            input_path = f_in.name

        oracle_out_path = input_path + ".oracle.txt"
        agent_out_path = input_path + ".agent.txt"

        try:
            subprocess.run([ORACLE_PATH, input_path, oracle_out_path], check=True, capture_output=True)
            subprocess.run([AGENT_PATH, input_path, agent_out_path], check=True, capture_output=True)

            with open(oracle_out_path, 'r') as f:
                oracle_output = f.read()

            with open(agent_out_path, 'r') as f:
                agent_output = f.read()

            assert oracle_output == agent_output, (
                f"Output mismatch on fuzz iteration {i}.\n"
                f"Seed: {42 + i}\n"
                f"Oracle output length: {len(oracle_output)}\n"
                f"Agent output length: {len(agent_output)}\n"
                f"Oracle output:\n{oracle_output[:500]}...\n"
                f"Agent output:\n{agent_output[:500]}..."
            )
        finally:
            for p in [input_path, oracle_out_path, agent_out_path]:
                if os.path.exists(p):
                    os.remove(p)