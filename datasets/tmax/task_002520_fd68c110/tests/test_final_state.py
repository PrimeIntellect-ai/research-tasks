# test_final_state.py

import os
import pytest

def test_pipeline_log_exists():
    """Verify that the pipeline log file was created."""
    log_path = '/home/user/pipeline.log'
    assert os.path.isfile(log_path), f"Log file missing at {log_path}"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "[INFO]" in content, "Log file does not contain expected '[INFO]' tags."
    assert "Pipeline completed" in content, "Log file does not indicate pipeline completion."

def test_mse_result_exists_and_correct():
    """Verify that the mse_result.txt exists and contains the correct MSE metric."""
    result_path = '/home/user/mse_result.txt'
    assert os.path.isfile(result_path), f"Result file missing at {result_path}"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        submitted_mse = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {result_path} as a float. Content was: '{content}'")

    # Re-derive expected MSE
    expected_values = [10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5, 35.0, 37.5, 40.0]
    reference_values = [10.2, 12.4, 15.1, 17.6, 20.0, 22.3, 25.0, 27.8, 30.1, 32.5, 34.9, 37.5, 40.2]

    sq_errors = [(e - r) ** 2 for e, r in zip(expected_values, reference_values)]
    expected_mse = sum(sq_errors) / len(expected_values)

    # Check against the threshold
    threshold = 0.5
    diff = abs(submitted_mse - expected_mse)
    assert diff < threshold, (
        f"Submitted MSE {submitted_mse} is too far from expected MSE {expected_mse:.4f}. "
        f"Difference {diff:.4f} exceeds threshold {threshold}."
    )