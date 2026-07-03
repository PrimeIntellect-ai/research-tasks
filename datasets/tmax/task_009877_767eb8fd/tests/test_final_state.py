# test_final_state.py

import os
import csv
import pytest

DATA_DIR = "/home/user/data"
REPORT_PATH = "/home/user/analysis_report.txt"
SCRIPT_PATH = "/home/user/analyze_spectroscopy.sh"

def compute_energy(filepath):
    total = 0.0
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader, start=1):
            if 10 <= r <= 40:
                for c, val in enumerate(row, start=1):
                    if 20 <= c <= 80:
                        total += float(val)
    return total

@pytest.fixture(scope="module")
def expected_results():
    baseline_path = os.path.join(DATA_DIR, "baseline.csv")
    baseline_energy = compute_energy(baseline_path)

    max_diff = 0.0
    for i in range(1, 11):
        run_path = os.path.join(DATA_DIR, f"run_{i}.csv")
        run_energy = compute_energy(run_path)
        diff = abs(baseline_energy - run_energy)
        if diff > max_diff:
            max_diff = diff

    conclusion = "REJECT_NULL" if max_diff > 0.05 else "ACCEPT_NULL"

    return {
        "baseline": f"{baseline_energy:.4f}",
        "max_diff": f"{max_diff:.4f}",
        "conclusion": conclusion
    }

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

def test_report_contents(expected_results):
    with open(REPORT_PATH, 'r') as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) == 3, f"Expected exactly 3 lines in {REPORT_PATH}, got {len(lines)}."

    expected_baseline_line = f"Baseline Energy: {expected_results['baseline']}"
    expected_max_diff_line = f"Max Difference: {expected_results['max_diff']}"
    expected_conclusion_line = f"Conclusion: {expected_results['conclusion']}"

    assert lines[0] == expected_baseline_line, f"Line 1 mismatch. Expected '{expected_baseline_line}', got '{lines[0]}'"
    assert lines[1] == expected_max_diff_line, f"Line 2 mismatch. Expected '{expected_max_diff_line}', got '{lines[1]}'"
    assert lines[2] == expected_conclusion_line, f"Line 3 mismatch. Expected '{expected_conclusion_line}', got '{lines[2]}'"