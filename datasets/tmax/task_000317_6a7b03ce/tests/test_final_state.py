# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle_analyzer"
AGENT_PATH = "/home/user/analyzer/target/release/analyzer"
NUM_TESTS = 200

def generate_fasta(seed):
    rng = random.Random(seed)
    seq_len = rng.randint(10, 500)
    seq = "".join(rng.choices(["A", "C", "G", "T"], k=seq_len))

    lines = [f">seq_{seed}"]
    for i in range(0, len(seq), 80):
        lines.append(seq[i:i+80])

    return "\n".join(lines) + "\n"

def test_seq_utils_tests_pass():
    """Verify that the vendored package's tests now pass."""
    assert os.path.isdir("/app/seq_utils"), "The /app/seq_utils directory is missing."
    res = subprocess.run(
        ["cargo", "test"],
        cwd="/app/seq_utils",
        capture_output=True,
        text=True
    )
    assert res.returncode == 0, f"cargo test failed in /app/seq_utils:\n{res.stdout}\n{res.stderr}"

def test_fuzz_equivalence():
    """Fuzz test the agent's binary against the oracle binary."""
    assert os.path.isfile(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle not executable at {ORACLE_PATH}"

    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary not executable at {AGENT_PATH}"

    for i in range(NUM_TESTS):
        fasta_input = generate_fasta(i)

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=fasta_input,
            text=True,
            capture_output=True,
            check=False
        )
        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=fasta_input,
            text=True,
            capture_output=True,
            check=False
        )

        oracle_out = oracle_proc.stdout
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on input {i}!\n"
                f"Input FASTA:\n{fasta_input}\n"
                f"Oracle Output: {repr(oracle_out)}\n"
                f"Agent Output: {repr(agent_out)}\n"
                f"Oracle stderr: {repr(oracle_proc.stderr)}\n"
                f"Agent stderr: {repr(agent_proc.stderr)}"
            )