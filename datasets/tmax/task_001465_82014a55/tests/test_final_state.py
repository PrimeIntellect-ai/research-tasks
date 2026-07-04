# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def generate_random_csv(seed):
    rng = random.Random(seed)

    num_metrics = rng.randint(1, 5)
    metrics = []
    for _ in range(num_metrics):
        metric_len = rng.randint(3, 8)
        metric = "".join(rng.choices(string.ascii_letters, k=metric_len))
        metrics.append(metric)

    header = ["host"] + metrics

    num_rows = rng.randint(1, 20)
    rows = []
    for _ in range(num_rows):
        host_len = rng.randint(5, 10)
        host = "".join(rng.choices(string.ascii_letters + string.digits, k=host_len))
        row = [host]
        for _ in range(num_metrics):
            choice = rng.random()
            if choice < 0.8:
                val = str(rng.randint(-10, 150))
            elif choice < 0.9:
                val = ""
            else:
                val_len = rng.randint(1, 5)
                val = "".join(rng.choices(string.ascii_letters, k=val_len))
            row.append(val)
        rows.append(row)

    lines = [",".join(header)]
    for r in rows:
        lines.append(",".join(r))

    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_transformer"
    agent_path = "/home/user/new_transformer"

    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    for i in range(100):
        csv_input = generate_random_csv(i)

        try:
            oracle_res = subprocess.run(
                [oracle_path],
                input=csv_input,
                text=True,
                capture_output=True,
                check=True
            )
            oracle_output = oracle_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {i}:\n{e.stderr}")

        try:
            agent_res = subprocess.run(
                [agent_path],
                input=csv_input,
                text=True,
                capture_output=True,
                check=True
            )
            agent_output = agent_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input {i}:\n{e.stderr}\nInput was:\n{csv_input}")

        if oracle_output != agent_output:
            pytest.fail(
                f"Output mismatch on input {i}.\n"
                f"Input:\n{csv_input}\n"
                f"Expected (Oracle):\n{oracle_output}\n"
                f"Got (Agent):\n{agent_output}"
            )