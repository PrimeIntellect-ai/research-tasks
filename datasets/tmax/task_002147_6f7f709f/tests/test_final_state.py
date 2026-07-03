# test_final_state.py

import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    agent_path = "/home/user/seq_score"
    oracle_path = "/app/oracle_seq_score"

    assert os.path.isfile(agent_path), f"Agent executable missing: {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent file is not executable: {agent_path}"

    assert os.path.isfile(oracle_path), f"Oracle executable missing: {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle file is not executable: {oracle_path}"

    random.seed(42)
    bases = ['A', 'C', 'G', 'T']

    for i in range(500):
        length = random.randint(10, 1000)
        seq = "".join(random.choices(bases, k=length))

        agent_proc = subprocess.run([agent_path], input=seq, text=True, capture_output=True)
        oracle_proc = subprocess.run([oracle_path], input=seq, text=True, capture_output=True)

        assert agent_proc.returncode == 0, f"Agent program failed with return code {agent_proc.returncode} on input {seq[:50]}..."
        assert oracle_proc.returncode == 0, f"Oracle program failed with return code {oracle_proc.returncode} on input {seq[:50]}..."

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        if agent_out != oracle_out:
            pytest.fail(f"Mismatch on input length {length} (showing first 50 chars: {seq[:50]}).\nExpected (Oracle): {oracle_out[:200]}...\nActual (Agent):  {agent_out[:200]}...")