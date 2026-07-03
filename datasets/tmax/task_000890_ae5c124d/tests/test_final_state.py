# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_fixed_encode_exists():
    assert os.path.isfile("/home/user/fixed_encode.py"), "The fixed python script /home/user/fixed_encode.py does not exist."

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_encoder"
    agent_script = "/home/user/fixed_encode.py"

    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} missing."
    assert os.path.isfile(agent_script), f"Agent script {agent_script} missing."

    # Generate printable characters excluding null byte
    # string.printable includes ascii_letters, digits, punctuation, and whitespace
    chars = [c for c in string.printable if c != '\0']

    random.seed(42)
    num_tests = 500

    for i in range(num_tests):
        length = random.randint(1, 100)
        test_input = "".join(random.choice(chars) for _ in range(length))

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path, test_input],
                capture_output=True,
                text=True,
                check=True
            )
            oracle_out = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle crashed on input {repr(test_input)}: {e.stderr}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                ["python3", agent_script, test_input],
                capture_output=True,
                text=True,
                check=True
            )
            agent_out = agent_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program crashed on input {repr(test_input)}.\nError: {e.stderr}")

        assert agent_out == oracle_out, (
            f"Mismatch on input: {repr(test_input)}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent):       {agent_out}"
        )