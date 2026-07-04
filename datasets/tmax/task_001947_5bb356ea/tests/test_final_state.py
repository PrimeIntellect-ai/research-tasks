# test_final_state.py

import os
import random
import struct
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_patch_transformer"
AGENT_PATH = "/home/user/patch_transformer"

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent path {AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent file {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"

    random.seed(42)
    N = 1000

    for i in range(N):
        # Generate random length between 16 and 1MB
        length = random.randint(16, 1000000)
        data = bytearray(random.randbytes(length))

        is_valid = random.choice([True, False])
        if is_valid:
            # Valid magic and payload length
            data[0:4] = b"PATC"
            payload_len = length - 16
            data[4:8] = struct.pack("<I", payload_len)
        else:
            # Malformed: either bad magic or bad length
            malform_type = random.choice(["bad_magic", "bad_length"])
            if malform_type == "bad_magic":
                data[0:4] = b"BADD"
                payload_len = length - 16
                data[4:8] = struct.pack("<I", payload_len)
            else:
                data[0:4] = b"PATC"
                # Require more bytes than available
                payload_len = length - 16 + random.randint(1, 1000)
                data[4:8] = struct.pack("<I", payload_len)

        input_bytes = bytes(data)

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_bytes,
            capture_output=True
        )

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_bytes,
            capture_output=True
        )

        # Compare exit codes
        assert agent_proc.returncode == oracle_proc.returncode, \
            f"Exit code mismatch on iteration {i} (valid_format={is_valid}, len={length}). " \
            f"Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        # Compare stdout (transformed data)
        assert agent_proc.stdout == oracle_proc.stdout, \
            f"Output mismatch on iteration {i} (valid_format={is_valid}, len={length}). " \
            f"Oracle output len: {len(oracle_proc.stdout)}, Agent output len: {len(agent_proc.stdout)}"