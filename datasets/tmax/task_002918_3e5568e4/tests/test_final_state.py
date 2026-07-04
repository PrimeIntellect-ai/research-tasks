# test_final_state.py

import os
import random
import subprocess
import tempfile
import uuid
import pytest

ORACLE_PATH = "/app/csv_processor"
AGENT_PATH = "/home/user/process.sh"

def generate_csv(filepath, num_rows):
    departments = ["Sales", "Engineering", "HR", "Marketing", "Support", "Finance", "Legal"]
    statuses = ["ACTIVE", "INACTIVE", "PENDING", "ARCHIVED"]

    with open(filepath, 'w') as f:
        f.write("id,department,status,revenue,cost,timestamp\n")
        for _ in range(num_rows):
            row_id = str(uuid.uuid4())
            dept = random.choice(departments)
            status = random.choice(statuses)
            revenue = round(random.uniform(0.0, 10000.0), 2)
            cost = round(random.uniform(0.0, 10000.0), 2)
            ts = f"2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}T{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}Z"
            f.write(f"{row_id},{dept},{status},{revenue},{cost},{ts}\n")

def test_agent_script_exists():
    """Verify the agent's script exists and is executable."""
    assert os.path.exists(AGENT_PATH), f"Agent script not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    """Fuzz both the oracle and the agent script to ensure exact equivalence."""
    random.seed(42)
    num_tests = 50

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(num_tests):
            num_rows = random.randint(0, 1000)
            csv_path = os.path.join(tmpdir, f"test_{i}.csv")
            generate_csv(csv_path, num_rows)

            oracle_cmd = [ORACLE_PATH, csv_path]
            agent_cmd = ["bash", AGENT_PATH, csv_path]

            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

            assert oracle_res.returncode == 0, f"Oracle failed on test case {i}:\n{oracle_res.stderr}"
            assert agent_res.returncode == 0, f"Agent script failed on test case {i}:\n{agent_res.stderr}"

            if oracle_res.stdout != agent_res.stdout:
                with open(csv_path, 'r') as f:
                    input_data = f.read()

                # Truncate input data for display if it's too large
                display_input = input_data if len(input_data) < 1000 else input_data[:1000] + "\n... [truncated]"

                pytest.fail(
                    f"Output mismatch on test case {i} (Rows: {num_rows}).\n\n"
                    f"=== Input CSV ===\n{display_input}\n\n"
                    f"=== Oracle Output ===\n{oracle_res.stdout}\n"
                    f"=== Agent Output ===\n{agent_res.stdout}\n"
                )