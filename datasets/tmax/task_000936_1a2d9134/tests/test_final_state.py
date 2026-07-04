# test_final_state.py
import os
import random
import subprocess
import gzip
import struct
import pytest

def generate_fuzz_input(seed):
    random.seed(seed)
    type_roll = random.random()
    if type_roll < 0.05:
        # Invalid gzip stream
        return bytes(random.getrandbits(8) for _ in range(100))

    # Valid gzip stream
    data = bytearray()
    if type_roll < 0.10:
        # Bad magic header
        bad_magics = [b"BART", b"ARTX", b"AAAA", b"1234"]
        data.extend(random.choice(bad_magics))
    else:
        # Correct magic header
        data.extend(b"ARTI")

    num_commands = random.randint(0, 5000)
    for _ in range(num_commands):
        op_roll = random.random()
        if op_roll < 0.5:
            # ADD (0x0A): 2-byte ID, 4-byte Size
            data.append(0x0A)
            data.extend(struct.pack("<H", random.randint(0, 50)))
            data.extend(struct.pack("<I", random.randint(0, 100000)))
        elif op_roll < 0.75:
            # REMOVE (0x0B): 2-byte ID
            data.append(0x0B)
            data.extend(struct.pack("<H", random.randint(0, 50)))
        else:
            # UPDATE (0x0C): 2-byte ID, 4-byte Size
            data.append(0x0C)
            data.extend(struct.pack("<H", random.randint(0, 50)))
            data.extend(struct.pack("<I", random.randint(0, 100000)))

    # 10% chance of truncation (if there's payload beyond the magic header)
    if random.random() < 0.10 and len(data) > 4:
        truncate_amount = random.randint(1, min(6, len(data) - 4))
        data = data[:-truncate_amount]

    return gzip.compress(data)

def test_fuzz_equivalence():
    agent_prog = "/home/user/wal_state_parser"
    oracle_prog = "/app/oracle_parser"

    assert os.path.isfile(agent_prog), f"Missing agent program: {agent_prog}"
    assert os.access(agent_prog, os.X_OK), f"Agent program is not executable: {agent_prog}"

    for i in range(1000):
        input_data = generate_fuzz_input(i)

        oracle_proc = subprocess.run(
            [oracle_prog],
            input=input_data,
            capture_output=True
        )

        agent_proc = subprocess.run(
            [agent_prog],
            input=input_data,
            capture_output=True
        )

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Return code mismatch on seed {i}.\n"
            f"Oracle exited with {oracle_proc.returncode}, agent exited with {agent_proc.returncode}."
        )
        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Stdout mismatch on seed {i}.\n"
            f"Oracle stdout:\n{oracle_proc.stdout.decode('utf-8', errors='replace')}\n"
            f"Agent stdout:\n{agent_proc.stdout.decode('utf-8', errors='replace')}"
        )