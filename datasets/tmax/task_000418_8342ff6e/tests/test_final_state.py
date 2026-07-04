# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_random_csv():
    num_rows = random.randint(1, 20)
    lines = ["text_data,base_prior"]
    for _ in range(num_rows):
        num_tokens = random.randint(1, 10)
        tokens = []
        for _ in range(num_tokens):
            token_len = random.randint(1, 150)
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=token_len))
            tokens.append(token)
        text_data = "|".join(tokens)
        base_prior = round(random.uniform(0.01, 0.99), 4)
        lines.append(f"{text_data},{base_prior}")
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/app/risk_oracle"
    agent_script = "/home/user/solution.py"

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.path.isfile(agent_script), f"Solution script not found at {agent_script}"

    random.seed(42)

    for i in range(50):
        input_csv = generate_random_csv()

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_csv,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=input_csv,
            text=True,
            capture_output=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed on input {i}. Stderr:\n{agent_proc.stderr}")

        agent_output = agent_proc.stdout

        if oracle_output != agent_output:
            pytest.fail(
                f"Mismatch on random input {i}.\n\n"
                f"Input:\n{input_csv}\n\n"
                f"Oracle Output:\n{oracle_output}\n\n"
                f"Agent Output:\n{agent_output}"
            )