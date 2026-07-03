# test_final_state.py
import os
import re
import pytest

def test_find_stable_step_script_exists_and_executable():
    script_path = "/home/user/app/find_stable_step.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_stability_log_exists():
    log_path = "/home/user/app/stability_log.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

def test_stability_log_content():
    log_path = "/home/user/app/stability_log.txt"
    with open(log_path, "r") as f:
        content = f.read().strip()

    # Check the format and values
    # Expected: Stable h: 0.0125, Max Val: 1.000000
    match = re.search(r"Stable h:\s*([0-9.]+),\s*Max Val:\s*([0-9.]+)", content)
    assert match is not None, f"Log file content '{content}' does not match the required format 'Stable h: <found_h>, Max Val: <max_absolute_value>'."

    found_h = float(match.group(1))
    max_val = float(match.group(2))

    assert abs(found_h - 0.0125) < 1e-6, f"Expected stable h to be 0.0125, but found {found_h}."
    assert abs(max_val - 1.0) < 1e-2, f"Expected max value to be around 1.0, but found {max_val}."