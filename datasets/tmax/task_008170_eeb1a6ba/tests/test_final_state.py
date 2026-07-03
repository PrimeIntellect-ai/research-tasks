# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_run_directory_exists():
    run_dir = "/home/user/runs/test_run"
    assert os.path.isdir(run_dir), f"Run directory {run_dir} does not exist. Did you run the script with 'test_run'?"

def test_invalid_log_content():
    log_path = "/home/user/runs/test_run/invalid.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["ds4_invalid.json", "ds6_invalid.json"]
    assert lines == expected_lines, f"Expected {expected_lines} in invalid.log, but got {lines}."

def test_metrics_txt_content():
    metrics_path = "/home/user/runs/test_run/metrics.txt"
    assert os.path.isfile(metrics_path), f"File {metrics_path} does not exist."

    with open(metrics_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Total: 6",
        "Valid: 4",
        "Invalid: 2"
    ]
    assert lines == expected_lines, f"Expected {expected_lines} in metrics.txt, but got {lines}."

def test_recommendations_tsv_content():
    tsv_path = "/home/user/runs/test_run/recommendations.tsv"
    assert os.path.isfile(tsv_path), f"File {tsv_path} does not exist."

    with open(tsv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "d1\td2\t0.50",
        "d2\td1\t0.50",
        "d3\td5\t0.25",
        "d5\td3\t0.25"
    ]
    assert lines == expected_lines, f"Expected {expected_lines} in recommendations.tsv, but got {lines}."