# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def generate_random_input():
    length = random.randint(0, 50)
    chars = string.ascii_letters + string.digits + " "
    text = "".join(random.choice(chars) for _ in range(length))
    v0 = random.uniform(-100.0, 100.0)
    v1 = random.uniform(-100.0, 100.0)
    v2 = random.uniform(-100.0, 100.0)
    return f"{text}|{v0},{v1},{v2}"

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_cleaner"
    agent_script = "/home/user/replicated_cleaner.py"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} not found."
    assert os.path.isfile(agent_script), f"Agent script {agent_script} not found."

    random.seed(42)

    N = 1000
    for _ in range(N):
        input_data = generate_random_input() + "\n"

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_path],
                input=input_data,
                text=True,
                capture_output=True,
                check=True
            )
            oracle_out = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {input_data.strip()}: {e.stderr}")

        # Run agent
        try:
            agent_res = subprocess.run(
                ["/usr/bin/python3", agent_script],
                input=input_data,
                text=True,
                capture_output=True,
                check=True
            )
            agent_out = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input {input_data.strip()}: {e.stderr}")

        assert oracle_out == agent_out, (
            f"Mismatch on input: {input_data.strip()}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output:  {agent_out}"
        )