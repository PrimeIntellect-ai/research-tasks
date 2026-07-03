# test_final_state.py

import os
import random
import subprocess
import pytest

AGENT_BINARY = "/home/user/archive_tool"
ORACLE_BINARY = "/app/oracle_archive_tool"

def generate_fuzz_inputs(n=1000):
    random.seed(42)
    inputs = []
    for _ in range(n):
        if random.random() < 0.1:
            # Pure random bytes
            length = random.randint(0, 8192)
            data = bytearray(random.getrandbits(8) for _ in range(length))
            inputs.append(bytes(data))
        else:
            # Structured archive
            data = bytearray()
            # 50% start with BACK
            if random.random() < 0.5:
                data += b"BACK"
            else:
                data += b"BORK"

            num_entries = random.randint(0, 15)
            for _ in range(num_entries):
                name_len = random.randint(1, 50)
                name = bytearray(random.choice(b"abcdefghijklmnopqrstuvwxyz./") for _ in range(name_len))

                # Inject "../" to test zip slip logic
                if random.random() < 0.3 and name_len >= 3:
                    idx = random.randint(0, name_len - 3)
                    name[idx:idx+3] = b"../"

                file_size = random.randint(0, 500)

                data += name_len.to_bytes(2, 'little')
                data += name
                data += file_size.to_bytes(4, 'little')
                data += bytearray(random.getrandbits(8) for _ in range(file_size))

            # Randomly truncate
            if random.random() < 0.2 and len(data) > 0:
                trunc_len = random.randint(0, len(data))
                data = data[:trunc_len]

            inputs.append(bytes(data))
    return inputs

def test_agent_binary_exists():
    assert os.path.exists(AGENT_BINARY), f"Student's tool is missing: {AGENT_BINARY}"
    assert os.path.isfile(AGENT_BINARY), f"Path is not a file: {AGENT_BINARY}"
    assert os.access(AGENT_BINARY, os.X_OK), f"Student's tool is not executable: {AGENT_BINARY}"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BINARY), "Oracle binary missing"
    assert os.path.exists(AGENT_BINARY), "Agent binary missing"

    inputs = generate_fuzz_inputs(1000)

    for i, data in enumerate(inputs):
        oracle_proc = subprocess.run(
            [ORACLE_BINARY],
            input=data,
            capture_output=True
        )

        agent_proc = subprocess.run(
            [AGENT_BINARY],
            input=data,
            capture_output=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Exit code mismatch on input {i} (len {len(data)}).\n"
            f"Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}\n"
            f"Oracle stdout: {oracle_proc.stdout!r}\n"
            f"Agent stdout: {agent_proc.stdout!r}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on input {i} (len {len(data)}).\n"
            f"Oracle stdout: {oracle_proc.stdout!r}\n"
            f"Agent stdout: {agent_proc.stdout!r}"
        )