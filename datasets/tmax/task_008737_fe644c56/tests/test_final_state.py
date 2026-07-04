# test_final_state.py
import os
import json
import subprocess
import math

def test_recovered_ts():
    path = "/home/user/uptime_monitor/recovered_ts.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == "2023-11-05 01:23:45", f"Expected '2023-11-05 01:23:45', but got '{content}'"

def test_report_json():
    path = "/home/user/uptime_monitor/report.json"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run generate_report.py?"
    with open(path, 'r') as f:
        data = json.load(f)

    assert "uptime_percentage" in data, "report.json missing 'uptime_percentage' key."

    expected_uptime = 100.0 * (1.0 - (1.0 / 14400.0))
    actual_uptime = data["uptime_percentage"]

    assert math.isclose(actual_uptime, expected_uptime, rel_tol=1e-9), \
        f"Expected uptime_percentage to be close to {expected_uptime}, but got {actual_uptime}. " \
        "Check your DST calculation and floating point summation."

def test_pytest_suite():
    test_file = "/home/user/uptime_monitor/test_monitor.py"
    assert os.path.isfile(test_file), f"File {test_file} does not exist."

    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest on {test_file} failed with output:\n{result.stdout}\n{result.stderr}"