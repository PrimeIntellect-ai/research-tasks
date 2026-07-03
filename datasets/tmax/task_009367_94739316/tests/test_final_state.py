# test_final_state.py

import os
import json
import pytest

def test_ci_pipeline_script_exists():
    """Check that the ci_pipeline.py script exists."""
    script_path = "/home/user/ci_pipeline.py"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."

def test_binaries_built():
    """Check that both binaries were successfully built and are executable."""
    bin_x86 = "/home/user/bin/worker_x86"
    bin_arm = "/home/user/bin/worker_arm"

    assert os.path.isfile(bin_x86), f"Binary {bin_x86} was not built."
    assert os.access(bin_x86, os.X_OK), f"Binary {bin_x86} is not executable."

    assert os.path.isfile(bin_arm), f"Binary {bin_arm} was not built."
    assert os.access(bin_arm, os.X_OK), f"Binary {bin_arm} is not executable."

def test_memory_report_exists_and_valid():
    """Check that the memory report exists and is valid JSON."""
    report_path = "/home/user/memory_report.json"
    assert os.path.isfile(report_path), f"Memory report {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert isinstance(data, dict), "JSON report should be a dictionary."

def test_memory_report_contents():
    """Check that the memory report contains the correct keys and values."""
    report_path = "/home/user/memory_report.json"
    if not os.path.isfile(report_path):
        pytest.skip("Memory report does not exist.")

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Memory report is not valid JSON.")

    expected_keys = {"worker_x86", "worker_arm", "leak_detected"}
    assert set(data.keys()) == expected_keys, f"JSON report keys do not match expected. Found: {list(data.keys())}"

    assert data["leak_detected"] == "worker_arm", "Incorrect leak_detected value. Expected 'worker_arm'."

    assert isinstance(data["worker_x86"], int), "worker_x86 value must be an integer."
    assert isinstance(data["worker_arm"], int), "worker_arm value must be an integer."

    assert data["worker_arm"] > 40000, f"worker_arm peak RSS too low ({data['worker_arm']} KB), expected > 40000 KB."
    assert data["worker_x86"] < 10000, f"worker_x86 peak RSS too high ({data['worker_x86']} KB), expected < 10000 KB."