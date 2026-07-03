# test_final_state.py

import os
import random
import string
import subprocess
import pytest

AGENT_BINARY = "/home/user/backup_parser"
ORACLE_BINARY = "/opt/oracle/backup_parser_oracle"

def generate_fuzz_input():
    chars = string.ascii_lowercase + string.digits + "_-"
    mount_len = random.randint(4, 12)
    mount = "".join(random.choices(chars, k=mount_len))

    used_bytes = random.randint(1000, 99999999)
    total_bytes = random.randint(100000, 9999999999)

    return f"{mount} {used_bytes} {total_bytes}\n"

def test_agent_binary_exists_and_executable():
    assert os.path.exists(AGENT_BINARY), f"The binary {AGENT_BINARY} does not exist."
    assert os.path.isfile(AGENT_BINARY), f"{AGENT_BINARY} is not a file."
    assert os.access(AGENT_BINARY, os.X_OK), f"The file {AGENT_BINARY} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BINARY), f"Oracle binary {ORACLE_BINARY} missing."

    random.seed(42)
    N = 500

    for i in range(N):
        fuzz_input = generate_fuzz_input()

        oracle_proc = subprocess.run(
            [ORACLE_BINARY],
            input=fuzz_input,
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, "Oracle failed on input."
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run(
            [AGENT_BINARY],
            input=fuzz_input,
            capture_output=True,
            text=True
        )

        assert agent_proc.returncode == 0, f"Agent binary failed (exit code {agent_proc.returncode}) on input: {fuzz_input.strip()}"
        agent_out = agent_proc.stdout

        assert agent_out == oracle_out, (
            f"Mismatch on iteration {i+1}.\n"
            f"Input: {fuzz_input!r}\n"
            f"Expected (Oracle): {oracle_out!r}\n"
            f"Got (Agent): {agent_out!r}"
        )