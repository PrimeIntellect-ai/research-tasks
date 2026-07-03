# test_final_state.py

import os
import subprocess
import random
import csv
import tempfile
import json
import pytest

ORACLE_PATH = "/app/legacy_reporter"
AGENT_SCRIPT = "/home/user/processor.py"
NUM_RUNS = 50

@pytest.fixture(scope="module")
def fuzzed_inputs():
    random.seed(42)
    inputs = []
    for _ in range(NUM_RUNS):
        num_rows = random.randint(5, 50)
        rows = []
        for i in range(1, num_rows + 1):
            txn_id = i
            user_id = random.randint(1, 5)
            timestamp = random.randint(100000, 1000000)
            amount = round(random.uniform(-100.0, 100.0), 2)
            rows.append({
                "txn_id": txn_id,
                "user_id": user_id,
                "timestamp": timestamp,
                "amount": amount
            })
        random.shuffle(rows)
        inputs.append(rows)
    return inputs

def test_agent_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"

def test_fuzz_equivalence(fuzzed_inputs):
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"

    for idx, rows in enumerate(fuzzed_inputs):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
            writer = csv.DictWriter(tmp, fieldnames=["txn_id", "user_id", "timestamp", "amount"])
            writer.writeheader()
            writer.writerows(rows)
            tmp_path = tmp.name

        try:
            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_PATH, tmp_path],
                capture_output=True,
                text=True,
                check=False
            )
            assert oracle_proc.returncode == 0, f"Oracle failed on run {idx} with input:\n{rows}\nStderr: {oracle_proc.stderr}"

            # Run agent
            agent_proc = subprocess.run(
                ["python3", AGENT_SCRIPT, tmp_path],
                capture_output=True,
                text=True,
                check=False
            )
            assert agent_proc.returncode == 0, f"Agent script failed on run {idx} with input:\n{rows}\nStderr: {agent_proc.stderr}"

            # Compare JSON outputs
            try:
                oracle_json = json.loads(oracle_proc.stdout)
            except json.JSONDecodeError:
                pytest.fail(f"Oracle output is not valid JSON on run {idx}: {oracle_proc.stdout}")

            try:
                agent_json = json.loads(agent_proc.stdout)
            except json.JSONDecodeError:
                pytest.fail(f"Agent output is not valid JSON on run {idx}: {agent_proc.stdout}")

            assert oracle_json == agent_json, (
                f"Mismatch on run {idx}!\n"
                f"Input CSV rows:\n{rows}\n\n"
                f"Oracle Output:\n{oracle_json}\n\n"
                f"Agent Output:\n{agent_json}"
            )
        finally:
            os.remove(tmp_path)