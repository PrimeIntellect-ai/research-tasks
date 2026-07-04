# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def test_auth_backend_fuzz_equivalence():
    oracle_path = "/app/auth_backend"
    agent_script = "/home/user/auth_backend.sh"

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} is missing."
    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."

    # Use a fixed seed for reproducibility
    random.seed(42)
    chars = string.ascii_letters + string.digits

    for _ in range(200):
        length = random.randint(8, 16)
        token = ''.join(random.choice(chars) for _ in range(length))

        oracle_cmd = [oracle_path, token]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=False)
        assert oracle_res.returncode == 0, f"Oracle failed on input '{token}'"
        expected_output = oracle_res.stdout

        agent_cmd = ["bash", agent_script, token]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=False)
        actual_output = agent_res.stdout

        assert expected_output == actual_output, (
            f"Mismatch on input '{token}'.\n"
            f"Expected (hex): {expected_output.hex()}\n"
            f"Actual (hex): {actual_output.hex()}"
        )