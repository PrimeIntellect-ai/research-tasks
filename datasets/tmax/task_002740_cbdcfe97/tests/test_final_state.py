# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def generate_random_input(seed):
    random.seed(seed)
    num_rows = random.randint(0, 50)
    lines = []

    for _ in range(num_rows):
        # SessionID
        if random.random() < 0.5:
            session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        else:
            session_id = ''.join(random.choices(string.printable, k=random.randint(1, 15))).replace('\t', '').replace('\n', '')

        # Metadata
        if random.random() < 0.5:
            num_newlines = random.randint(1, 5)
            inner_text = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=random.randint(5, 50)))
            # Insert newlines randomly into inner_text
            chars = list(inner_text)
            for _ in range(num_newlines):
                chars.insert(random.randint(0, len(chars)), '\n')
            metadata = f"<<{''.join(chars)}>>"
        else:
            metadata = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 20)))

        # Metrics
        num_metrics = random.randint(0, 10)
        metrics_list = []
        for _ in range(num_metrics):
            if random.random() < 0.1:
                metrics_list.append("malformed_metric")
                continue

            key_len = random.randint(1, 10)
            key = ''.join(random.choices(string.ascii_letters + "ＣＡＦＥ温度!_ ", k=key_len))
            val = random.randint(-1000, 1000)
            metrics_list.append(f"{key}:{val}")

        metrics = ','.join(metrics_list)

        # 10% chance of malformed row (not 3 columns)
        if random.random() < 0.1:
            if random.random() < 0.5:
                row = f"{session_id}\t{metadata}"
            else:
                row = f"{session_id}\t{metadata}\t{metrics}\textra"
        else:
            row = f"{session_id}\t{metadata}\t{metrics}"

        lines.append(row)

    return '\n'.join(lines).encode('utf-8')

def test_fuzz_equivalence():
    oracle_path = "/app/log_analyzer"
    agent_path = "/home/user/solution"

    assert os.path.exists(agent_path), f"Agent solution missing at {agent_path}"
    assert os.path.isfile(agent_path), f"{agent_path} is not a file"
    assert os.access(agent_path, os.X_OK), f"{agent_path} is not executable"

    for i in range(200):
        input_data = generate_random_input(i)

        proc_oracle = subprocess.run([oracle_path], input=input_data, capture_output=True)
        proc_agent = subprocess.run([agent_path], input=input_data, capture_output=True)

        oracle_out = proc_oracle.stdout
        agent_out = proc_agent.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on input seed {i}.\n"
                f"Input data:\n{input_data.decode('utf-8', errors='replace')}\n"
                f"Oracle output:\n{oracle_out.decode('utf-8', errors='replace')}\n"
                f"Agent output:\n{agent_out.decode('utf-8', errors='replace')}"
            )