# test_final_state.py

import os
import csv
import json
import random
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/oracle_pipeline.py"
AGENT_PATH = "/home/user/pipeline.py"
TINYDB_STORAGES_PATH = "/app/tinydb-4.8.0/tinydb/storages.py"
EXPERIMENTS_DB_PATH = "/home/user/experiments.json"

def test_tinydb_fixed():
    """Verify that the vendored tinydb bug is fixed."""
    assert os.path.isfile(TINYDB_STORAGES_PATH), "tinydb storages.py is missing."
    with open(TINYDB_STORAGES_PATH, "r") as f:
        content = f.read()
    assert "import jsonn" not in content, "The bug 'import jsonn' is still present in tinydb/storages.py."

def test_pipeline_exists():
    """Verify the agent script exists."""
    assert os.path.isfile(AGENT_PATH), f"Agent script {AGENT_PATH} does not exist."

def test_fuzz_equivalence():
    """Generate 50 random pairs of CSVs and compare agent output to oracle output."""
    assert os.path.isfile(ORACLE_PATH), f"Oracle script {ORACLE_PATH} does not exist."

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(50):
            sensors_path = os.path.join(tmpdir, f"sensors_{i}.csv")
            predictions_path = os.path.join(tmpdir, f"predictions_{i}.csv")

            # Generate sensors.csv
            num_sensors = random.randint(50, 200)
            with open(sensors_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "actual_value"])
                for _ in range(num_sensors):
                    writer.writerow([random.randint(1, 1000), round(random.uniform(0.0, 100.0), 2)])

            # Generate predictions.csv
            num_preds = random.randint(50, 200)
            with open(predictions_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "pred_value", "threshold"])
                for _ in range(num_preds):
                    writer.writerow([
                        random.randint(1, 1000), 
                        round(random.uniform(0.0, 100.0), 2), 
                        round(random.uniform(0.5, 5.0), 2)
                    ])

            # Run oracle
            oracle_cmd = ["python3", ORACLE_PATH, sensors_path, predictions_path]
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
            assert oracle_res.returncode == 0, f"Oracle failed on iteration {i}:\n{oracle_res.stderr}"

            # Run agent
            agent_cmd = ["python3", AGENT_PATH, sensors_path, predictions_path]
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
            assert agent_res.returncode == 0, f"Agent script failed on iteration {i}:\n{agent_res.stderr}"

            # Compare STDOUT
            assert agent_res.stdout == oracle_res.stdout, (
                f"Output mismatch on iteration {i}.\n"
                f"Sensors file: {sensors_path}\n"
                f"Predictions file: {predictions_path}\n"
                f"Expected STDOUT:\n{oracle_res.stdout}\n"
                f"Got STDOUT:\n{agent_res.stdout}"
            )

def test_experiments_logged():
    """Verify that experiments.json is created and contains valid JSON."""
    assert os.path.isfile(EXPERIMENTS_DB_PATH), f"Experiments DB {EXPERIMENTS_DB_PATH} was not created."

    with open(EXPERIMENTS_DB_PATH, "r") as f:
        try:
            db_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{EXPERIMENTS_DB_PATH} is not valid JSON.")

    # TinyDB default format usually has a '_default' table
    assert "_default" in db_data, "TinyDB should have a '_default' table."
    records = db_data["_default"]
    assert len(records) > 0, "No experiment records found in the database."

    # Check the format of the last inserted record
    last_record = list(records.values())[-1]
    assert "sensors_file" in last_record, "Missing 'sensors_file' in experiment record."
    assert "predictions_file" in last_record, "Missing 'predictions_file' in experiment record."
    assert "valid_count" in last_record, "Missing 'valid_count' in experiment record."
    assert isinstance(last_record["valid_count"], int), "'valid_count' must be an integer."