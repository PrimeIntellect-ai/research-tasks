# test_final_state.py

import os
import subprocess
import random
import string
import struct
import bz2
import pytest

def generate_random_string(min_len=3, max_len=15):
    length = random.randint(min_len, max_len)
    chars = string.ascii_letters + string.digits + "_.-"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_journal(num_entries=50):
    data = bytearray()
    for _ in range(num_entries):
        opcode = random.choice([0, 1, 2])
        data.append(opcode)
        if opcode == 0:
            n = random.randint(1, 20)
            data.extend(struct.pack("<H", n))
            for _ in range(n):
                data.extend(generate_random_string().encode('ascii') + b'\x00')
                data.extend(generate_random_string().encode('ascii') + b'\x00')
        elif opcode == 1:
            data.extend(generate_random_string().encode('ascii') + b'\x00')
            data.extend(generate_random_string().encode('ascii') + b'\x00')
        elif opcode == 2:
            data.extend(generate_random_string().encode('ascii') + b'\x00')
            data.extend(generate_random_string().encode('ascii') + b'\x00')
    return bz2.compress(data)

def test_executable_exists():
    agent_exe = "/home/user/journal_compiler"
    assert os.path.isfile(agent_exe), f"Agent executable not found at {agent_exe}"
    assert os.access(agent_exe, os.X_OK), f"Agent file at {agent_exe} is not executable"

def test_fuzz_equivalence():
    oracle_exe = "/opt/oracle/journal_compiler_oracle"
    agent_exe = "/home/user/journal_compiler"

    assert os.path.isfile(oracle_exe), f"Oracle executable not found at {oracle_exe}"

    random.seed(42)

    for i in range(100):
        compressed_journal = generate_random_journal(num_entries=random.randint(10, 100))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_exe],
            input=compressed_journal,
            capture_output=True,
            timeout=5
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"

        # Run agent
        agent_proc = subprocess.run(
            [agent_exe],
            input=compressed_journal,
            capture_output=True,
            timeout=5
        )

        assert agent_proc.returncode == 0, f"Agent program failed (return code {agent_proc.returncode}) on fuzz input {i}"

        oracle_out = oracle_proc.stdout.decode('utf-8', errors='replace')
        agent_out = agent_proc.stdout.decode('utf-8', errors='replace')

        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on fuzz input {i}.\n"
                f"--- Oracle Output ---\n{oracle_out}\n"
                f"--- Agent Output ---\n{agent_out}\n"
            )