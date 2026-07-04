# test_final_state.py

import os
import subprocess
import tempfile
import pytest

SCRIPT_PATH = "/home/user/evaluate_experiments.sh"
BASELINE_PATH = "/home/user/baseline.csv"
NEW_MODEL_PATH = "/home/user/new_model.csv"
REPORT_PATH = "/home/user/experiment_report.txt"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_script_success_and_report_content():
    # Remove report if it exists to ensure the script generates it
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

    result = subprocess.run(
        [SCRIPT_PATH, BASELINE_PATH, NEW_MODEL_PATH],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    assert os.path.exists(REPORT_PATH), f"Report file not created at {REPORT_PATH}"

    with open(REPORT_PATH, "r") as f:
        report_content = f.read().strip()

    expected_content = (
        "Baseline Accuracy: 0.8000\n"
        "Baseline CI: [0.5521, 1.0479]\n"
        "New Model Accuracy: 1.0000"
    )

    assert report_content == expected_content, f"Report content mismatch.\nExpected:\n{expected_content}\nGot:\n{report_content}"

def test_script_reproducibility_error():
    # Create a dummy bad model with altered pca coordinates
    bad_model_content = """id,true_label,pred_label,pca1,pca2
1,1,1,0.5,0.1
2,0,0,0.2,0.999
3,1,1,0.8,0.3
4,0,0,0.1,0.4
5,1,1,0.9,0.2
6,0,0,0.3,0.3
7,1,1,0.4,0.4
8,0,0,0.5,0.5
9,1,1,0.6,0.6
10,0,0,0.7,0.7
"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        tmp.write(bad_model_content)
        bad_model_path = tmp.name

    try:
        result = subprocess.run(
            [SCRIPT_PATH, BASELINE_PATH, bad_model_path],
            capture_output=True,
            text=True
        )

        assert result.returncode == 1, f"Expected return code 1 for reproducibility error, got {result.returncode}"
        assert result.stdout.strip() == "Reproducibility Error", f"Expected stdout 'Reproducibility Error', got '{result.stdout.strip()}'"
    finally:
        os.remove(bad_model_path)