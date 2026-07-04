# test_final_state.py

import os
import subprocess
import re
import pytest

CSV_PATH = "/home/user/training_data.csv"
EVAL_SCRIPT = "/app/train_and_eval.py"

def test_training_data_csv_exists():
    assert os.path.isfile(CSV_PATH), f"Expected CSV file at {CSV_PATH} does not exist."

def test_training_data_csv_header():
    with open(CSV_PATH, 'r') as f:
        header = f.readline().strip()
    expected_header = "pdb_id,mean_dist,max_dist,var_dist,label"
    assert header == expected_header, f"CSV header is incorrect. Expected '{expected_header}', got '{header}'."

def test_model_accuracy_meets_threshold():
    # Run the evaluation script
    result = subprocess.run(
        ["python3", EVAL_SCRIPT, CSV_PATH],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Evaluation script failed with error:\n{result.stderr}"

    # Extract accuracy from standard output
    output = result.stdout
    match = re.search(r"Accuracy:\s*([0-9]*\.?[0-9]+)", output)
    assert match is not None, f"Could not parse 'Accuracy: <value>' from output:\n{output}"

    accuracy = float(match.group(1))
    threshold = 0.90

    assert accuracy >= threshold, f"Model accuracy {accuracy} is below the threshold of {threshold}."