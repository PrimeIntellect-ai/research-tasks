# test_final_state.py
import os
import random
import subprocess
import pytest

AGENT_PATH = "/home/user/rust_scorer/target/release/rust_scorer"
ORACLE_PATH = "/app/seq_align_scorer"
SCRIPT_PATH = "/home/user/test_scorer.sh"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_bash_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Bash script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent binary missing at {AGENT_PATH}"

    random.seed(42)
    chars = ['A', 'C', 'G', 'T']

    for i in range(1000):
        len1 = random.randint(5, 60)
        len2 = random.randint(5, 60)

        seq1 = "".join(random.choices(chars, k=len1))
        seq2 = "".join(random.choices(chars, k=len2))

        try:
            oracle_out = subprocess.check_output([ORACLE_PATH, seq1, seq2], text=True).strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on inputs: {seq1}, {seq2}")

        try:
            agent_out = subprocess.check_output([AGENT_PATH, seq1, seq2], text=True).strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent failed on inputs: {seq1}, {seq2}")

        assert agent_out == oracle_out, f"Mismatch on inputs: '{seq1}', '{seq2}'. Oracle: {oracle_out}, Agent: {agent_out}"