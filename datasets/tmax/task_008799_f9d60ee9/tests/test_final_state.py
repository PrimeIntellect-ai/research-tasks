# test_final_state.py

import os
import subprocess
import pytest

def test_service_c_recovered():
    recovered_path = "/home/user/logs/service_c_recovered.log"
    assert os.path.isfile(recovered_path), f"Recovered log file {recovered_path} is missing."

    with open(recovered_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "1698242520 Database query started",
        "1698242820 Database query completed"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' missing from {recovered_path}."

def test_unified_log_exists_and_correct():
    unified_path = "/home/user/logs/unified.log"
    assert os.path.isfile(unified_path), f"Unified log file {unified_path} is missing."

    with open(unified_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1698242400 ServiceA System initialized",
        "1698242460 ServiceB Authentication request received",
        "1698242520 ServiceC Database query started",
        "1698242700 ServiceA Connection established",
        "1698242760 ServiceB User logged in successfully",
        "1698242820 ServiceC Database query completed"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {unified_path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        # The prompt specifies the format as `[EPOCH] [SERVICE_NAME] [MESSAGE]`
        # We will check if the line matches the expected exactly, or with literal brackets if the user took it literally.
        # But the truth data shows no literal brackets.
        actual_stripped = actual.replace("[", "").replace("]", "")
        expected_stripped = expected.replace("[", "").replace("]", "")
        assert actual_stripped == expected_stripped, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."

def test_emitter_process_still_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "service_c_emitter"]).decode("utf-8")
        assert output.strip() != "", "service_c_emitter process is no longer running."
    except subprocess.CalledProcessError:
        pytest.fail("service_c_emitter process is no longer running (pgrep returned non-zero).")

def test_aggregate_script_exists():
    script_path = "/home/user/scripts/aggregate.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."