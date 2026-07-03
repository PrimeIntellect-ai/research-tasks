# test_final_state.py

import os
import stat
import random
import subprocess
import pytest

ORACLE_PATH = "/app/seq_scorer"
AGENT_PATH = "/home/user/my_scorer.sh"
NUM_TESTS = 200

def test_agent_script_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent script {AGENT_PATH} does not exist."
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file."

    st = os.stat(AGENT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Agent script {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} missing."

    random.seed(42)
    chars = ['A', 'C', 'G', 'T', 'N']

    for i in range(NUM_TESTS):
        length = random.randint(10, 1000)
        # Occasionally include 'N', but mostly 'A', 'C', 'G', 'T'
        # Let's just use the uniform choice from the list which includes 'N'
        seq = "".join(random.choice(chars) for _ in range(length))

        input_data = (seq + "\n").encode('utf-8')

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=input_data,
                capture_output=True,
                check=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout.decode('utf-8').strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input of length {length}.")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input of length {length}. Return code: {e.returncode}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=input_data,
                capture_output=True,
                check=False,
                timeout=2
            )
            agent_out = agent_proc.stdout.decode('utf-8').strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input:\n{seq}")

        assert agent_proc.returncode == 0, f"Agent script failed with return code {agent_proc.returncode} on input:\n{seq}\nStderr: {agent_proc.stderr.decode('utf-8')}"

        assert agent_out == oracle_out, (
            f"Mismatch on input of length {length}.\n"
            f"Input: {seq}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )