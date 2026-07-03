# test_final_state.py
import os
import csv
import json
import random
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/legacy_parser"
AGENT_PATH = "/home/user/process_data.py"

def generate_random_csv(num_rows):
    departments = ["Engineering", "Sales", "HR", "Marketing", "Finance"]

    # Generate unique employee IDs
    all_ids = random.sample(range(1, 1001), num_rows)

    rows = []
    generated_ids = []

    for i, emp_id in enumerate(all_ids):
        if i == 0:
            manager_id = ""
        else:
            # Pick a manager from previously generated to ensure valid tree/DAG
            manager_id = random.choice(generated_ids)

        dept = random.choice(departments)
        score = round(random.uniform(0.0, 100.0), 2)

        rows.append([emp_id, manager_id, dept, score])
        generated_ids.append(emp_id)

    # Shuffle rows so they are not strictly topologically sorted in the CSV
    random.shuffle(rows)
    return rows

@pytest.mark.parametrize("seed", range(50))
def test_fuzz_equivalence(seed):
    random.seed(seed)

    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent script missing at {AGENT_PATH}"

    num_rows = random.randint(10, 200)
    csv_data = generate_random_csv(num_rows)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        writer = csv.writer(tmp)
        writer.writerows(csv_data)
        tmp_path = tmp.name

    try:
        # Run oracle
        oracle_cmd = [ORACLE_PATH, tmp_path]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on seed {seed}:\n{oracle_res.stderr}"

        # Run agent
        agent_cmd = ["python3", AGENT_PATH, tmp_path]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent failed on seed {seed}:\n{agent_res.stderr}"

        # Parse JSON
        try:
            oracle_json = json.loads(oracle_res.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle output is not valid JSON on seed {seed}:\n{oracle_res.stdout}")

        try:
            agent_json = json.loads(agent_res.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Agent output is not valid JSON on seed {seed}:\n{agent_res.stdout}")

        # Compare
        assert agent_json == oracle_json, (
            f"Output mismatch on seed {seed}.\n"
            f"Input CSV:\n{csv_data}\n"
            f"Oracle JSON:\n{json.dumps(oracle_json, indent=2)}\n"
            f"Agent JSON:\n{json.dumps(agent_json, indent=2)}"
        )

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)