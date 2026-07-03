# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/primer_oracle"
AGENT_SCRIPT = "/home/user/my_primer_oracle.sh"
N_TESTS = 100
CHARSET = "ACGT"
MIN_LEN = 10
MAX_LEN = 50
SEED = 42

def test_agent_script_exists_and_executable():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"{AGENT_SCRIPT} is not executable"

def generate_random_sequences(n, min_len, max_len, charset, seed):
    random.seed(seed)
    sequences = []
    for _ in range(n):
        length = random.randint(min_len, max_len)
        seq = "".join(random.choice(charset) for _ in range(length))
        sequences.append(seq)
    return sequences

def run_command(cmd, arg):
    result = subprocess.run(
        [cmd, arg],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip(), result.returncode

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"

    sequences = generate_random_sequences(N_TESTS, MIN_LEN, MAX_LEN, CHARSET, SEED)

    for seq in sequences:
        oracle_out, oracle_rc = run_command(ORACLE_PATH, seq)
        agent_out, agent_rc = run_command(AGENT_SCRIPT, seq)

        assert agent_rc == oracle_rc, (
            f"Return code mismatch for input '{seq}'. "
            f"Oracle returned {oracle_rc}, Agent returned {agent_rc}"
        )

        assert agent_out == oracle_out, (
            f"Output mismatch for input '{seq}'.\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output:  '{agent_out}'"
        )