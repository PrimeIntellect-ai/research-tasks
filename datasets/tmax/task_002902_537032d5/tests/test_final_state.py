# test_final_state.py
import os
import random
import string
import struct
import subprocess
import pytest

def generate_fuzz_input(seed):
    random.seed(seed)
    out = bytearray()
    num_records = random.randint(0, 20)
    for _ in range(num_records):
        # Magic
        if random.random() < 0.9:
            magic = b"ARTF"
        else:
            magic = b"BADM"

        # Size
        if random.random() < 0.8:
            size = random.randint(0, 1024)
        else:
            size = random.randint(1025, 2000)

        # Flags
        r = random.random()
        if r < 0.3:
            flags = 142
        elif r < 0.6:
            flags = random.choice([0, 1, 2, 3])
        else:
            flags = random.randint(0, 65535)

        # Name
        name_len = random.randint(1, 16)
        name_str = "".join(random.choices(string.ascii_letters + string.digits, k=name_len))
        name = name_str.encode('ascii').ljust(16, b'\0')

        # Data
        data = bytes(random.choices(range(256), k=size))

        record = magic + struct.pack("<IH", size, flags) + name + data
        out.extend(record)

    # Premature truncation
    if random.random() < 0.1 and len(out) > 0:
        trunc_len = random.randint(0, len(out) - 1)
        out = out[:trunc_len]

    return bytes(out)

def run_program(executable, input_data):
    try:
        result = subprocess.run(
            [executable],
            input=input_data,
            capture_output=True,
            timeout=2
        )
        return result.returncode, result.stdout
    except subprocess.TimeoutExpired:
        return -999, b"TIMEOUT"

def test_fuzz_equivalence():
    oracle = "/app/oracle_curator"
    agent = "/home/user/repo_curator"

    assert os.path.isfile(agent), f"Agent program not found at {agent}"
    assert os.access(agent, os.X_OK), f"Agent program is not executable at {agent}"
    assert os.path.isfile(oracle), f"Oracle program not found at {oracle}"

    # Run a large number of fuzz iterations
    N = 1000
    for i in range(N):
        input_data = generate_fuzz_input(i)

        oracle_rc, oracle_out = run_program(oracle, input_data)
        agent_rc, agent_out = run_program(agent, input_data)

        error_msg = (
            f"Mismatch on fuzz seed {i}!\n"
            f"Input length: {len(input_data)} bytes\n"
            f"Input hex (first 100 bytes): {input_data[:100].hex()}...\n"
            f"Oracle return code: {oracle_rc}\n"
            f"Agent return code: {agent_rc}\n"
            f"Oracle stdout: {oracle_out}\n"
            f"Agent stdout: {agent_out}\n"
        )

        assert oracle_rc == agent_rc, f"Return code mismatch: {error_msg}"
        assert oracle_out == agent_out, f"Stdout mismatch: {error_msg}"