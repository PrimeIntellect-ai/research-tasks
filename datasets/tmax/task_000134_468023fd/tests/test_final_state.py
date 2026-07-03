# test_final_state.py

import os
import random
import subprocess
import pytest

AGENT_EXE = '/home/user/seq_analyzer_fixed'
ORACLE_EXE = '/app/oracle_seq_analyzer'
N_ITERATIONS = 100

def test_executable_exists():
    assert os.path.isfile(AGENT_EXE), f"Agent executable {AGENT_EXE} does not exist."
    assert os.access(AGENT_EXE, os.X_OK), f"Agent executable {AGENT_EXE} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_EXE), f"Oracle executable {ORACLE_EXE} does not exist."
    assert os.access(ORACLE_EXE, os.X_OK), f"Oracle executable {ORACLE_EXE} is not executable."

    random.seed(42)
    bases = ['A', 'T', 'C', 'G']

    for i in range(N_ITERATIONS):
        length = random.randint(100, 1000)
        dna_seq = ''.join(random.choices(bases, k=length))

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [ORACLE_EXE, dna_seq],
                capture_output=True,
                text=True,
                check=True
            )
            oracle_out = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on iteration {i} with input length {length}. Stderr: {e.stderr}")

        # Run agent
        try:
            agent_res = subprocess.run(
                [AGENT_EXE, dna_seq],
                capture_output=True,
                text=True,
                check=True
            )
            agent_out = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on iteration {i} with input length {length}. Stderr: {e.stderr}")

        assert agent_out == oracle_out, (
            f"Output mismatch on iteration {i} with input length {length}.\n"
            f"Input: {dna_seq}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )