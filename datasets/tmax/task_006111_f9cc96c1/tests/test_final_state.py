# test_final_state.py

import os
import json
import pytest

def test_telemetry_dat_content():
    """Verify that telemetry.dat exists and has the correct content."""
    filepath = '/home/user/telemetry.dat'
    assert os.path.exists(filepath), f"File {filepath} does not exist."

    expected_content = (
        "HEAD\n"
        "0A 14 1E\n"
        "05 0F\n"
        "END\n"
        "HEAD\n"
        "FF 00\n"
        "ERROR_LINE\n"
        "END\n"
        "HEAD\n"
        "02 04 06 08\n"
        "END\n"
    )

    with open(filepath, 'r') as f:
        content = f.read()

    # Normalize line endings for comparison
    assert content.strip() == expected_content.strip(), f"Content of {filepath} does not match expected."

def test_process_telemetry_script_exists():
    """Verify that process_telemetry.py exists."""
    filepath = '/home/user/process_telemetry.py'
    assert os.path.exists(filepath), f"File {filepath} does not exist."

def test_results_json():
    """Verify that results.json exists and contains the correct metrics."""
    filepath = '/home/user/results.json'
    assert os.path.exists(filepath), f"File {filepath} does not exist. Did you run the script?"

    with open(filepath, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {filepath} is not valid JSON.")

    assert isinstance(results, list), f"Expected results.json to contain a list, got {type(results).__name__}."
    assert len(results) == 2, f"Expected 2 frames in results.json, found {len(results)}."

    # Verify Frame 0
    frame_0 = results[0]
    assert frame_0.get("frame_id") == 0, f"Expected frame_id 0, got {frame_0.get('frame_id')}."
    metrics_0 = frame_0.get("metrics", {})
    assert abs(metrics_0.get("mean", 0) - 16.0) < 1e-6, f"Expected mean 16.0 for frame 0, got {metrics_0.get('mean')}."
    assert abs(metrics_0.get("variance", 0) - 74.0) < 1e-6, f"Expected variance 74.0 for frame 0, got {metrics_0.get('variance')}."

    # Verify Frame 1
    frame_1 = results[1]
    assert frame_1.get("frame_id") == 1, f"Expected frame_id 1, got {frame_1.get('frame_id')}."
    metrics_1 = frame_1.get("metrics", {})
    assert abs(metrics_1.get("mean", 0) - 5.0) < 1e-6, f"Expected mean 5.0 for frame 1, got {metrics_1.get('mean')}."
    assert abs(metrics_1.get("variance", 0) - 5.0) < 1e-6, f"Expected variance 5.0 for frame 1, got {metrics_1.get('variance')}."