# test_final_state.py
import os
import json
import pytest

def test_executable_exists():
    executable_path = "/home/user/bio_project/src/gc_calc"
    assert os.path.exists(executable_path), f"Executable {executable_path} not found. Did you compile the C code?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_report_content():
    report_path = "/home/user/bio_project/report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} not found."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(lines) >= 4, "report.txt is missing required lines."

    # Compute expected means from golden_gc.json
    golden_file = "/home/user/bio_project/data/golden_gc.json"
    assert os.path.exists(golden_file), f"Data file {golden_file} is missing."

    with open(golden_file, "r") as f:
        golden = json.load(f)

    case_gcs = [v for k, v in golden.items() if k.startswith("case_")]
    control_gcs = [v for k, v in golden.items() if k.startswith("control_")]

    expected_case_mean = sum(case_gcs) / len(case_gcs)
    expected_control_mean = sum(control_gcs) / len(control_gcs)

    expected_lines = [
        "Regression: PASS",
        f"Control Mean: {expected_control_mean:.4f}",
        f"Case Mean: {expected_case_mean:.4f}",
        "P-value: 0.0002"
    ]

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Mismatch at line {i+1} in report.txt. Expected '{expected}', got '{lines[i]}'"