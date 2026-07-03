# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

ORACLE_PATH = "/app/legacy_oracle"
AGENT_PATH = "/home/user/parser.sh"
N_FUZZ = 500

def generate_fuzz_file(path, category):
    """
    Categories:
    0: Valid custom audio header (starts with AUDI)
    1: Corrupted header (random mutations in first 16 bytes, not AUDI)
    2: Purely random binary fuzz data
    3: File too short (< 16 bytes)
    """
    if category == 0:
        length = random.randint(16, 4096)
        content = bytearray(random.getrandbits(8) for _ in range(length))
        content[0:4] = b"AUDI"
    elif category == 1:
        length = random.randint(16, 4096)
        content = bytearray(random.getrandbits(8) for _ in range(length))
        content[0:4] = b"CORR" # explicitly corrupt
    elif category == 2:
        length = random.randint(16, 4096)
        content = bytearray(random.getrandbits(8) for _ in range(length))
        if content[0:4] == b"AUDI":
            content[0] = 0x00
    elif category == 3:
        length = random.randint(0, 15)
        content = bytearray(random.getrandbits(8) for _ in range(length))

    with open(path, "wb") as f:
        f.write(content)

def run_program(executable, input_path):
    try:
        result = subprocess.run(
            [executable, input_path],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -2, "", str(e)

def test_parser_exists_and_executable():
    assert os.path.isfile(AGENT_PATH), f"Missing agent script: {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script is not executable: {AGENT_PATH}"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Missing legacy oracle: {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Legacy oracle is not executable: {ORACLE_PATH}"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(N_FUZZ):
            rand_val = random.random()
            if rand_val < 0.2:
                category = 0
            elif rand_val < 0.6:
                category = 1
            elif rand_val < 0.9:
                category = 2
            else:
                category = 3

            test_file = os.path.join(tmpdir, f"fuzz_{i}.bin")
            generate_fuzz_file(test_file, category)

            oracle_code, oracle_out, oracle_err = run_program(ORACLE_PATH, test_file)
            agent_code, agent_out, agent_err = run_program(AGENT_PATH, test_file)

            error_msg = (
                f"Mismatch on fuzz input {i} (category {category}, size {os.path.getsize(test_file)}).\n"
                f"Oracle exited with {oracle_code}, Agent exited with {agent_code}.\n"
                f"Oracle stdout:\n{oracle_out}\n"
                f"Agent stdout:\n{agent_out}\n"
                f"Oracle stderr:\n{oracle_err}\n"
                f"Agent stderr:\n{agent_err}\n"
            )

            assert oracle_code == agent_code, error_msg
            assert oracle_out == agent_out, error_msg
            # We don't strictly assert stderr equivalence unless specified, but stdout and exit code must match.