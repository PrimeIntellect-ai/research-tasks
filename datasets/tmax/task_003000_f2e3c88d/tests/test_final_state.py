# test_final_state.py

import os
import json
import subprocess
import sys

def test_fixed_output():
    output_file = '/home/user/fixed_output.txt'
    assert os.path.isfile(output_file), f"{output_file} does not exist."
    with open(output_file, 'r') as f:
        content = f.read().strip()
    assert "Total alerts: 1" in content, f"Expected 'Total alerts: 1' in {output_file}, but got: {content}"

def test_timeline_json():
    timeline_file = '/home/user/timeline.json'
    assert os.path.isfile(timeline_file), f"{timeline_file} does not exist."

    with open(timeline_file, 'r') as f:
        try:
            timeline = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{timeline_file} is not valid JSON."

    expected_timeline = [
        {"timestamp": 1700000000, "service": "app", "message": "Service started"},
        {"timestamp": 1700000005, "service": "monitor", "message": "Monitor started"},
        {"timestamp": 1700000010, "service": "app", "message": "Ping OK"},
        {"timestamp": 1700000015, "service": "monitor", "message": "Processed early pings"},
        {"timestamp": 1700000020, "service": "app", "message": "Ping OK"},
        {"timestamp": 1700000090, "service": "app", "message": "Ping OK"},
        {"timestamp": 1700000100, "service": "app", "message": "Ping OK"},
        {"timestamp": 1700000105, "service": "monitor", "message": "Crash imminent"}
    ]

    assert isinstance(timeline, list), "Timeline must be a JSON array."
    assert len(timeline) == len(expected_timeline), f"Expected {len(expected_timeline)} events, got {len(timeline)}."

    for i, (actual, expected) in enumerate(zip(timeline, expected_timeline)):
        assert actual == expected, f"Event at index {i} mismatch. Expected {expected}, got {actual}."

def test_monitor_py_fixed():
    # Test that running monitor.py does not raise IndexError and exits cleanly
    monitor_script = '/home/user/sre_app/monitor.py'
    assert os.path.isfile(monitor_script), f"{monitor_script} does not exist."

    result = subprocess.run([sys.executable, monitor_script], capture_output=True, text=True)
    assert result.returncode == 0, f"monitor.py failed to run. Stderr: {result.stderr}"
    assert "Total alerts: 1" in result.stdout, "monitor.py output did not contain the correct alert count."

def test_test_monitor_py():
    test_script = '/home/user/sre_app/test_monitor.py'
    assert os.path.isfile(test_script), f"{test_script} does not exist."

    with open(test_script, 'r') as f:
        content = f.read()

    assert "check_gaps" in content, "test_monitor.py does not import or use check_gaps."

    # Run the test file using pytest
    result = subprocess.run([sys.executable, "-m", "pytest", test_script], capture_output=True, text=True)
    if result.returncode != 0:
        # Fallback to python execution in case it's a standard unittest script with __main__ block
        result_unittest = subprocess.run([sys.executable, test_script], capture_output=True, text=True)
        assert result_unittest.returncode == 0, f"Tests in {test_script} failed to pass. Pytest stderr: {result.stderr}\nUnittest stderr: {result_unittest.stderr}"