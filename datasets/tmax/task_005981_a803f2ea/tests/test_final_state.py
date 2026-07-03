# test_final_state.py

import os
import math
import pytest

def test_simulate_go_exists():
    path = "/home/user/simulate.go"
    assert os.path.isfile(path), f"Missing file: {path}. The task requires saving the Go program as simulate.go."

def test_regression_report_content():
    report_path = "/home/user/regression_report.txt"
    assert os.path.isfile(report_path), f"Missing file: {report_path}. The report was not generated."

    # Calculate the expected historical P95 from the reference data
    ref_path = "/home/user/reference_data.txt"
    assert os.path.isfile(ref_path), f"Missing reference data file: {ref_path}"

    with open(ref_path, "r") as f:
        data = [float(line.strip()) for line in f if line.strip()]

    data.sort()
    idx = math.ceil(0.95 * len(data)) - 1
    hist_p95 = data[idx]

    expected_hist_str = f"{hist_p95:.2f}"
    # The simulated P95 is deterministic based on the Go 1.20+ rand package with seed 42
    expected_sim_str = "520.25"

    if float(expected_sim_str) > 1.20 * hist_p95:
        expected_status = "REGRESSION DETECTED"
    else:
        expected_status = "PERFORMANCE OK"

    expected_content = f"Historical P95: {expected_hist_str}\nSimulated P95: {expected_sim_str}\nStatus: {expected_status}"

    with open(report_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The content of {report_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )