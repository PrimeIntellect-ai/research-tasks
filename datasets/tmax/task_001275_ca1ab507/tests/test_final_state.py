# test_final_state.py

import os
import csv
import subprocess
import pytest

def test_virtual_environment_exists():
    python_path = "/home/user/mlops_env/bin/python"
    assert os.path.isfile(python_path), f"Virtual environment Python executable not found at {python_path}"

    # Check if pandas is installed in the virtual environment
    result = subprocess.run([python_path, "-m", "pip", "show", "pandas"], capture_output=True, text=True)
    assert result.returncode == 0, "pandas is not installed in the virtual environment"

def test_script_exists():
    script_path = "/home/user/summarize_artifacts.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

def test_experiment_summary_csv():
    csv_path = "/home/user/experiment_summary.csv"
    assert os.path.isfile(csv_path), f"Summary CSV not found at {csv_path}"

    expected_rows = [
        {"run_id": "run_beta", "learning_rate": "0.001", "final_accuracy": "0.89", "model_size_bytes": "2048"},
        {"run_id": "run_gamma", "learning_rate": "0.005", "final_accuracy": "0.82", "model_size_bytes": "1536"},
        {"run_id": "run_alpha", "learning_rate": "0.01", "final_accuracy": "0.78", "model_size_bytes": "1024"}
    ]

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        assert fieldnames == ["run_id", "learning_rate", "final_accuracy", "model_size_bytes"], \
            f"CSV columns are incorrect. Expected ['run_id', 'learning_rate', 'final_accuracy', 'model_size_bytes'], got {fieldnames}"

        rows = list(reader)

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(rows)} in the CSV"

    for i, (expected, actual) in enumerate(zip(expected_rows, rows)):
        assert actual["run_id"] == expected["run_id"], f"Row {i+1}: expected run_id {expected['run_id']}, got {actual['run_id']}"
        assert float(actual["learning_rate"]) == float(expected["learning_rate"]), f"Row {i+1}: expected learning_rate {expected['learning_rate']}, got {actual['learning_rate']}"
        assert float(actual["final_accuracy"]) == float(expected["final_accuracy"]), f"Row {i+1}: expected final_accuracy {expected['final_accuracy']}, got {actual['final_accuracy']}"
        assert int(actual["model_size_bytes"]) == int(expected["model_size_bytes"]), f"Row {i+1}: expected model_size_bytes {expected['model_size_bytes']}, got {actual['model_size_bytes']}"