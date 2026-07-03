# test_final_state.py

import os
import random
import string
import subprocess
import pytest
import csv
import io

AGENT_SCRIPT = "/home/user/process_data"
ORACLE_SCRIPT = "/app/reference_oracle.py"
CRON_FILE = "/home/user/schedule.cron"
NUM_ITERATIONS = 500

def generate_random_csv(num_rows=10):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["record_id", "operator_name", "temp_morning", "temp_afternoon", "temp_evening"])
    for _ in range(num_rows):
        record_id = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(4, 10)))
        operator_name = "".join(random.choices(string.ascii_letters, k=random.randint(3, 15)))
        temp_morning = f"{random.uniform(-50.0, 50.0):.2f}"
        temp_afternoon = f"{random.uniform(-50.0, 50.0):.2f}"
        temp_evening = f"{random.uniform(-50.0, 50.0):.2f}"
        writer.writerow([record_id, operator_name, temp_morning, temp_afternoon, temp_evening])
    return output.getvalue()

def test_cron_schedule():
    assert os.path.exists(CRON_FILE), f"Cron schedule file missing at {CRON_FILE}"
    with open(CRON_FILE, "r") as f:
        content = f.read().strip()
    assert content == "15 4 1 * *", f"Expected cron expression '15 4 1 * *', got '{content}'"

def test_process_data_executable():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script at {AGENT_SCRIPT} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_SCRIPT), f"Oracle script missing at {ORACLE_SCRIPT}"

    random.seed(42)

    for i in range(NUM_ITERATIONS):
        csv_input = generate_random_csv(num_rows=random.randint(1, 20))

        oracle_proc = subprocess.run(
            [ORACLE_SCRIPT],
            input=csv_input,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_output = oracle_proc.stdout

        agent_proc = subprocess.run(
            [AGENT_SCRIPT],
            input=csv_input,
            text=True,
            capture_output=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed with return code {agent_proc.returncode}.\nStderr: {agent_proc.stderr}")

        agent_output = agent_proc.stdout

        if agent_output != oracle_output:
            pytest.fail(
                f"Mismatch found on iteration {i+1}!\n"
                f"Input CSV:\n{csv_input}\n"
                f"Expected Output (Oracle):\n{oracle_output}\n"
                f"Actual Output (Agent):\n{agent_output}"
            )