# test_final_state.py

import os
import sys
import random
import string
import subprocess
import pytest

def generate_random_csv(seed):
    random.seed(seed)
    num_rows = random.randint(10, 100)
    server_ids = ['srv1', 'srv2', 'srv3']

    lines = []

    # 50% chance to have a header
    if random.choice([True, False]):
        lines.append("timestamp,server_id,message")

    for _ in range(num_rows):
        num_cols = random.randint(1, 5)
        row = []
        for c in range(num_cols):
            if c == 1 and num_cols == 3:
                # 80% chance to use a valid server id
                if random.random() < 0.8:
                    row.append(random.choice(server_ids))
                else:
                    row.append("".join(random.choices(string.ascii_letters, k=4)))
            else:
                # Random text with spaces, newlines, quotes
                length = random.randint(0, 50)
                chars = string.ascii_letters + string.digits + " \n\t"
                text = "".join(random.choices(chars, k=length))

                # Format as CSV field (quote if contains comma, newline, quote)
                if any(x in text for x in [',', '\n', '"']):
                    text = '"' + text.replace('"', '""') + '"'
                row.append(text)
        lines.append(",".join(row))

    return "\n".join(lines)

def test_fuzz_equivalence():
    agent_script = "/home/user/log_analyzer.py"
    oracle_script = "/opt/oracle/log_analyzer_oracle.py"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} is missing."

    env = os.environ.copy()
    env["PYTHONPATH"] = "/app/py_custom_csv-0.1:" + env.get("PYTHONPATH", "")

    for i in range(200):
        csv_data = generate_random_csv(i)

        # Run oracle
        oracle_proc = subprocess.run(
            [sys.executable, oracle_script],
            input=csv_data,
            text=True,
            capture_output=True,
            env=env
        )

        # Run agent
        agent_proc = subprocess.run(
            [sys.executable, agent_script],
            input=csv_data,
            text=True,
            capture_output=True,
            env=env
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed with return code {agent_proc.returncode} on input seed {i}.\nStderr: {agent_proc.stderr}")

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(f"Output mismatch on input seed {i}.\n\nInput CSV:\n{csv_data}\n\nOracle stdout:\n{oracle_proc.stdout}\n\nAgent stdout:\n{agent_proc.stdout}")