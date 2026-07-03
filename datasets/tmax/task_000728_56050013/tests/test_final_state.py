# test_final_state.py

import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    agent_script = "/home/user/seq_splitter.py"
    oracle_binary = "/app/seq_domain_splitter"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(oracle_binary), f"Oracle binary {oracle_binary} does not exist."

    random.seed(42)
    chars = ['A', 'C', 'G', 'T']
    N = 200

    for i in range(N):
        length = random.randint(20, 500)
        seq = "".join(random.choices(chars, k=length))

        # Run oracle
        oracle_res = subprocess.run(
            [oracle_binary, seq],
            capture_output=True,
            text=True,
            check=True
        )
        oracle_out = oracle_res.stdout

        # Run agent
        agent_res = subprocess.run(
            ["python3", agent_script, seq],
            capture_output=True,
            text=True
        )

        if agent_res.returncode != 0:
            pytest.fail(f"Agent script failed on input of length {length}.\nInput: {seq}\nStderr: {agent_res.stderr}")

        agent_out = agent_res.stdout

        assert agent_out == oracle_out, (
            f"Output mismatch on input of length {length}.\n"
            f"Input: {seq}\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output:  {repr(agent_out)}"
        )