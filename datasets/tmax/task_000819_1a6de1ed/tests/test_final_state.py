# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fixed_processor_equivalence():
    agent_executable = "/home/user/fixed_processor"
    oracle_executable = "/app/oracle_processor"

    assert os.path.isfile(agent_executable), f"Agent executable {agent_executable} does not exist."
    assert os.access(agent_executable, os.X_OK), f"Agent executable {agent_executable} is not executable."
    assert os.path.isfile(oracle_executable), f"Oracle executable {oracle_executable} does not exist."

    random.seed(42)
    num_rounds = 5000

    for _ in range(num_rounds):
        length = random.randint(2, 50)
        sequence = [str(random.randint(0, 1000)) for _ in range(length)]
        input_str = ",".join(sequence)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_executable, input_str],
            capture_output=True,
            text=True,
            check=False
        )

        # Run agent
        agent_proc = subprocess.run(
            [agent_executable, input_str],
            capture_output=True,
            text=True,
            check=False
        )

        assert agent_proc.returncode == oracle_proc.returncode, \
            f"Return code mismatch on input '{input_str}'. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, \
            f"Output mismatch on input '{input_str}'.\nExpected (Oracle): {oracle_out}\nGot (Agent): {agent_out}"