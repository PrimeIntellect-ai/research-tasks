# test_final_state.py
import os
import subprocess
import random
import string
import csv
import io
import pytest

ORACLE_PATH = "/app/log_oracle"
AGENT_PATH = "/home/user/solution"
N_TESTS = 200

def generate_csv_input(seed):
    random.seed(seed)
    num_rows = random.randint(10, 500)

    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["timestamp", "message", "metric"])

    seen_messages = []

    for _ in range(num_rows):
        timestamp = random.randint(1600000000, 1600000500)

        if seen_messages and random.random() < 0.20:
            message = random.choice(seen_messages)
        else:
            length = random.randint(5, 20)
            chars = string.ascii_letters + string.digits
            message = "".join(random.choice(chars) for _ in range(length))

            if random.random() < 0.10:
                # Insert a newline somewhere in the message
                insert_pos = random.randint(0, len(message))
                message = message[:insert_pos] + "\n" + message[insert_pos:]

            seen_messages.append(message)

        metric = random.randint(0, 100)
        writer.writerow([timestamp, message, metric])

    return output.getvalue().encode('utf-8')

def test_solution_exists():
    assert os.path.exists(AGENT_PATH), f"Agent solution binary missing at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent solution path {AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent solution binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH)
    assert os.path.exists(AGENT_PATH)

    for i in range(N_TESTS):
        csv_data = generate_csv_input(seed=42 + i)

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=csv_data,
            capture_output=True,
            timeout=5
        )
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=csv_data,
            capture_output=True,
            timeout=5
        )
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            error_msg = (
                f"Mismatch on test case {i+1}!\n\n"
                f"--- INPUT CSV ---\n{csv_data.decode('utf-8')[:500]}...\n\n"
                f"--- ORACLE STDOUT ---\n{oracle_out.decode('utf-8', errors='replace')}\n\n"
                f"--- AGENT STDOUT ---\n{agent_out.decode('utf-8', errors='replace')}\n\n"
                f"Oracle stderr: {oracle_proc.stderr.decode('utf-8', errors='replace')}\n"
                f"Agent stderr: {agent_proc.stderr.decode('utf-8', errors='replace')}\n"
            )
            pytest.fail(error_msg)