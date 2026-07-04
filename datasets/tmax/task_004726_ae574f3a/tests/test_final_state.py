# test_final_state.py

import os
import subprocess
import random
import pytest

def test_fast_primer_exists_and_executable():
    agent_path = "/home/user/fast_primer.py"
    assert os.path.exists(agent_path), f"Agent script {agent_path} is missing."
    assert os.path.isfile(agent_path), f"{agent_path} is not a file."
    assert os.access(agent_path, os.X_OK), f"Agent script {agent_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_primer"
    agent_path = "/home/user/fast_primer.py"

    assert os.path.exists(oracle_path), f"Oracle {oracle_path} missing."

    random.seed(42)
    bases = ['A', 'C', 'G', 'T']

    num_tests = 1000

    for _ in range(num_tests):
        length = random.randint(20, 100)
        dna_seq = "".join(random.choices(bases, k=length))

        oracle_proc = subprocess.run([oracle_path, dna_seq], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_path, dna_seq], capture_output=True, text=True)

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch on input {dna_seq}. Expected {oracle_proc.returncode}, got {agent_proc.returncode}."

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, f"Output mismatch on input {dna_seq}.\nOracle output:\n{oracle_out}\n\nAgent output:\n{agent_out}"