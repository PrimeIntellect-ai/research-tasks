# test_final_state.py

import os
import json
import pytest

def test_files_moved_correctly():
    """Verify that libstate.so and events.txt were moved to their new locations."""
    assert os.path.isfile('/home/user/project/bin/libstate.so'), "Shared library libstate.so was not moved to /home/user/project/bin/"
    assert not os.path.exists('/home/user/project/lib/libstate.so'), "Shared library libstate.so still exists in the old location"

    assert os.path.isfile('/home/user/project/archive/events.txt'), "Data file events.txt was not moved to /home/user/project/archive/"
    assert not os.path.exists('/home/user/project/data/events.txt'), "Data file events.txt still exists in the old location"

def test_python_script_contents():
    """Verify that process_events.py exists and contains the required elements."""
    script_path = '/home/user/project/process_events.py'
    assert os.path.isfile(script_path), f"Python script {script_path} is missing"

    with open(script_path, 'r') as f:
        code = f.read()

    assert "unittest.TestCase" in code, "unittest.TestCase is missing from the Python script"
    assert "TestFFIWrapper" in code, "TestFFIWrapper class is missing from the Python script"
    assert "c_char_p" in code, "ctypes.c_char_p is missing from the Python script"
    assert "c_int" in code, "ctypes.c_int is missing from the Python script"
    assert "process_event" in code, "process_event function reference is missing from the Python script"

def test_results_json():
    """Verify that results.json exists and has the correct output."""
    results_path = '/home/user/project/results.json'
    assert os.path.isfile(results_path), f"{results_path} is missing"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} is not a valid JSON file")

    expected = {
        "evt1": 0,
        "evt2": 2,
        "evt3": -2,
        "evt4": 0,
        "evt5": 1
    }

    assert results == expected, f"Expected {expected}, got {results}"