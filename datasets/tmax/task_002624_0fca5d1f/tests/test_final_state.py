# test_final_state.py

import os
import json
import pytest

def test_etl_script_exists():
    """Check if the etl_check.py script exists."""
    script_path = "/home/user/etl_check.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_etl_script_numpy_config():
    """Check if the script configures numpy to raise exceptions for invalid and divide errors."""
    script_path = "/home/user/etl_check.py"
    with open(script_path, "r") as f:
        content = f.read()

    # We look for something like np.seterr(invalid='raise', divide='raise')
    # or similar configurations.
    assert "invalid" in content and "raise" in content, "Script does not seem to configure numpy to raise on 'invalid' errors."
    assert "divide" in content and "raise" in content, "Script does not seem to configure numpy to raise on 'divide' errors."

def test_output_report_exists():
    """Check if the output report JSON exists."""
    report_path = "/home/user/output/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

def test_output_report_content():
    """Check if the output report contains the correct calculated values."""
    report_path = "/home/user/output/report.json"

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "condition_number" in report, "Report missing 'condition_number' key."
    assert "mse" in report, "Report missing 'mse' key."

    # Recompute expected values
    try:
        import numpy as np
    except ImportError:
        pytest.fail("numpy is not installed in the test environment.")

    X = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 10.0],
        [1.5, 2.5, 3.5]
    ], dtype=np.float64)
    y = np.array([10.0, 20.0, 30.0, 12.0], dtype=np.float64)

    expected_cond = np.linalg.cond(X)
    w, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    preds = X @ w
    expected_mse = np.mean((y - preds) ** 2)

    assert abs(report["condition_number"] - expected_cond) < 1e-3, f"Condition number mismatch: {report['condition_number']} != {expected_cond}"
    assert abs(report["mse"] - expected_mse) < 1e-3, f"MSE mismatch: {report['mse']} != {expected_mse}"