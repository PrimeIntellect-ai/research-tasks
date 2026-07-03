# test_final_state.py

import os
import random
import struct
import subprocess
import pytest

def test_libwalparse_a_exists():
    assert os.path.isfile('/app/libwalparse-1.0/libwalparse.a'), "libwalparse.a was not built"

def test_archiver_executable_exists():
    assert os.path.isfile('/home/user/archiver'), "/home/user/archiver executable is missing"
    assert os.access('/home/user/archiver', os.X_OK), "/home/user/archiver is not executable"

def generate_fuzz_input():
    # Generate a random binary stream ranging from 0 to 8192 bytes.
    # Mix of valid WAL frames and random noise.
    length = random.randint(0, 8192)
    out = bytearray()

    while len(out) < length:
        choice = random.random()
        if choice < 0.3:
            # Add random noise
            noise_len = random.randint(1, 100)
            out.extend(random.randbytes(noise_len))
        else:
            # Add valid frame
            magic = 0x57414C21
            page_id = random.randint(0, 0xFFFFFFFF)
            data_len = random.randint(0, 256)
            data = random.randbytes(data_len)

            # Pack: magic (big-endian or little-endian? The problem says "magic 0x57414C21". Let's pack as big-endian for magic to match the hex literal if it's read byte-by-byte, or little endian. Actually, let's just pack as struct.pack('>I', 0x57414C21) to be safe, or '<I'. The problem statement says "magic 0x57414C21". We will try big-endian.
            # Wait, usually magic numbers are written in big-endian in specs. Let's provide both or let random noise cover the alternative.
            # Let's pack it as big-endian.
            frame = struct.pack('>I', magic) + struct.pack('<I', page_id) + struct.pack('<H', data_len) + data
            out.extend(frame)

    return bytes(out[:length])

def test_fuzz_equivalence():
    oracle_path = '/opt/oracle/wal_archiver'
    agent_path = '/home/user/archiver'

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"

    random.seed(42)
    N = 500

    for i in range(N):
        input_data = generate_fuzz_input()

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            capture_output=True,
            timeout=2
        )
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=input_data,
            capture_output=True,
            timeout=2
        )
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input length: {len(input_data)}\n"
                f"Oracle output length: {len(oracle_out)}\n"
                f"Agent output length: {len(agent_out)}\n"
                f"Oracle output (hex): {oracle_out.hex()}\n"
                f"Agent output (hex): {agent_out.hex()}"
            )