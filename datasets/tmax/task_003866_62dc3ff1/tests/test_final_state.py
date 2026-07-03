# test_final_state.py

import json
import os
import pytest

def test_anomaly_timestamps_mae():
    """Verify the detected anomaly timestamps against the ground truth using MAE."""
    target_file = "/home/user/anomaly_timestamps.json"

    assert os.path.exists(target_file), f"Output file is missing: {target_file}"
    assert os.path.isfile(target_file), f"Output path is not a file: {target_file}"

    try:
        with open(target_file, "r") as f:
            detected = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to parse JSON from {target_file}: {e}")

    assert isinstance(detected, list), f"Expected a JSON array, got {type(detected).__name__}"

    # Ensure all elements are numbers
    for val in detected:
        assert isinstance(val, (int, float)), f"Expected numbers in JSON array, got {type(val).__name__}: {val}"

    truth = [14.2, 42.6, 89.0]

    detected = sorted(detected)
    truth = sorted(truth)

    error_sum = 0.0

    for d in detected:
        if not truth:
            break
        closest = min(truth, key=lambda t: abs(t - d))
        error_sum += abs(closest - d)

    # Penalties for length mismatch
    penalty = abs(len(detected) - len(truth)) * 10.0
    error_sum += penalty

    mae = error_sum / max(len(truth), 1)

    threshold = 1.0
    assert mae <= threshold, f"MAE {mae:.2f} exceeds threshold of {threshold:.2f}. Detected: {detected}, Truth: {truth}"