# test_final_state.py
import os
import csv
import re

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_artifacts.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_report_exists():
    report_path = "/home/user/artifact_report.txt"
    assert os.path.isfile(report_path), f"Report {report_path} does not exist."

def test_report_content():
    csv_path = "/home/user/artifacts.csv"
    report_path = "/home/user/artifact_report.txt"

    assert os.path.isfile(csv_path), f"Data file {csv_path} is missing."

    # Compute true mean of memory_mb to validate the report
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        memory_vals = [float(row['memory_mb']) for row in reader]

    true_mean = sum(memory_vals) / len(memory_vals)

    with open(report_path, 'r') as f:
        content = f.read()

    assert "Primary Feature: memory_mb" in content, "Report missing or incorrect 'Primary Feature'. Expected 'memory_mb'."

    expected_true_mean_str = f"True Mean: {true_mean:.2f}"
    assert expected_true_mean_str in content, f"Report missing or incorrect 'True Mean'. Expected '{expected_true_mean_str}'."

    assert "Accuracy Check Passed: Yes" in content, "Report missing or incorrect 'Accuracy Check Passed'. Expected 'Yes'."

    # Extract Bootstrap Grand Mean and verify it's within tolerance
    match = re.search(r"Bootstrap Grand Mean:\s*([0-9.]+)", content)
    assert match is not None, "Could not find 'Bootstrap Grand Mean' value in the report."

    bootstrap_mean = float(match.group(1))
    assert abs(true_mean - bootstrap_mean) < 0.5, f"Bootstrap mean {bootstrap_mean} is not within 0.5 of true mean {true_mean}."