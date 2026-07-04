# test_final_state.py

import os
import random
import pytest

def generate_data(seed):
    random.seed(seed)
    num_points = random.randint(95, 105)
    return [random.gauss(40, 10) if random.random() < 0.5 else random.gauss(80, 10) for _ in range(num_points)]

def find_threshold(data):
    threshold = sum(data) / len(data)
    for _ in range(100):
        low = [x for x in data if x <= threshold]
        high = [x for x in data if x > threshold]

        if not low or not high:
            break

        new_threshold = (sum(low)/len(low) + sum(high)/len(high)) / 2.0

        if abs(new_threshold - threshold) < 0.001: 
            break

        threshold = new_threshold
    else:
        raise ValueError("Convergence failed")

    return threshold

def test_diagnostics_report():
    report_path = "/home/user/diagnostics_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 50, f"Expected 50 lines in the report, but found {len(lines)}."

    expected_lines = []
    for seed in range(1, 51):
        data = generate_data(seed)
        thresh = find_threshold(data)
        expected_lines.append(f"Seed {seed}: {thresh:.2f}")

    for i, (actual, expected) in enumerate(zip(lines, expected_lines), 1):
        assert actual == expected, f"Mismatch at line {i}. Expected: '{expected}', Actual: '{actual}'"

def test_script_is_fixed():
    script_path = "/home/user/forensics/log_analyzer.py"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # Check that the old bug 1 is gone or fixed
    assert "chunk = [data[i+j] for j in range(chunk_size)]" not in content, "The chunking IndexError bug is still present."

    # Check that the old bug 2 is fixed
    assert "abs(" in content or "abs (" in content, "The convergence bug (missing abs() in threshold check) does not appear to be fixed."