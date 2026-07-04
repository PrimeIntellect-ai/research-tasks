# test_final_state.py

import os
import subprocess
import random
import pytest
import csv

def test_virtual_environment_exists():
    venv_python = "/home/user/venv/bin/python"
    assert os.path.isfile(venv_python), f"Virtual environment Python not found at {venv_python}. Did you create the venv?"

    # Check if a package from requirements was installed successfully
    result = subprocess.run([venv_python, "-c", "import requests"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to import 'requests' in the virtual environment. Dependencies might not be resolved correctly."

def test_database_recovery():
    csv_path = "/home/user/recovered_events.csv"
    assert os.path.isfile(csv_path), f"Recovered events CSV not found at {csv_path}"

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # The WAL file contained 5 recent records. The CSV should have those records (plus optionally a header).
    # Just check that we have at least 5 rows and 3 columns (id, timestamp, event_name).
    assert len(rows) >= 5, f"Expected at least 5 rows in {csv_path}, found {len(rows)}"
    for row in rows:
        if row == ['id', 'timestamp', 'event_name']:
            continue
        assert len(row) == 3, f"Expected 3 columns in CSV row, but got: {row}"

def test_fuzz_equivalence():
    oracle_path = "/app/time_oracle"
    agent_script = "/home/user/processor.py"

    assert os.path.isfile(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"

    random.seed(42)
    num_tests = 1000

    for _ in range(num_tests):
        timestamp = str(random.randint(0, 2000000000))

        # Run oracle
        oracle_res = subprocess.run([oracle_path, timestamp], capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {timestamp}"
        oracle_out = oracle_res.stdout.strip()

        # Run agent script
        agent_res = subprocess.run(["python3", agent_script, timestamp], capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on input {timestamp}. Stderr: {agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on timestamp {timestamp}.\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output:  {agent_out}"
        )