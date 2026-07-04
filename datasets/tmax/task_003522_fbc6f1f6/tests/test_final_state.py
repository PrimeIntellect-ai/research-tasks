# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_run_processor_exists():
    assert os.path.isfile("/home/user/run_processor.py"), "/home/user/run_processor.py is missing"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_processor.py"
    agent_path = "/home/user/run_processor.py"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent script missing at {agent_path}"

    random.seed(42)
    charset = string.ascii_letters + string.digits

    num_tests = 500

    for _ in range(num_tests):
        length = random.randint(0, 100)
        test_input = ''.join(random.choice(charset) for _ in range(length))

        # Run oracle
        try:
            oracle_result = subprocess.run(
                ["python3", oracle_path, test_input],
                capture_output=True,
                text=True,
                check=True
            )
            oracle_output = oracle_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input: {test_input!r}\nError: {e.stderr}")

        # Run agent
        try:
            agent_result = subprocess.run(
                ["python3", agent_path, test_input],
                capture_output=True,
                text=True,
                check=True
            )
            agent_output = agent_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input: {test_input!r}\nError: {e.stderr}")

        assert agent_output == oracle_output, (
            f"Mismatch on input: {test_input!r}\n"
            f"Expected (Oracle): {oracle_output!r}\n"
            f"Got (Agent): {agent_output!r}"
        )