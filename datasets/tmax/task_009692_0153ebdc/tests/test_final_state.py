# test_final_state.py

import os
import json
import subprocess
import pytest

def test_parsed_output():
    output_path = "/home/user/parsed_output.json"
    assert os.path.exists(output_path), f"{output_path} does not exist. Ensure the script was run and generated the output."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} is not valid JSON.")

    assert isinstance(data, list), "Parsed output should be a JSON list."
    assert len(data) == 9, f"Expected 9 parsed items in the JSON output, found {len(data)}."

    for i, item in enumerate(data):
        assert "version" in item, f"Missing 'version' key in parsed item at index {i}."
        assert "data" in item, f"Missing 'data' key in parsed item at index {i}."
        assert item["version"] in ["v1", "v2"], f"Invalid version value in parsed item at index {i}."

def test_regression_script_execution():
    script_path = "/home/user/test_parser.py"
    assert os.path.exists(script_path), f"{script_path} does not exist. You must write a regression test."

    # Run the test script
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, (
        f"test_parser.py failed to execute successfully (exit code {result.returncode}).\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

def test_suspicious_parser_execution_no_deadlock():
    script_path = "/home/user/suspicious_parser.py"
    assert os.path.exists(script_path), f"{script_path} does not exist."

    try:
        # Run the parser with a timeout to detect deadlocks
        result = subprocess.run(["python3", script_path], capture_output=True, text=True, timeout=5)
        assert result.returncode == 0, (
            f"suspicious_parser.py failed to execute (exit code {result.returncode}).\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
    except subprocess.TimeoutExpired:
        pytest.fail("suspicious_parser.py timed out after 5 seconds. The deadlock issue is likely not resolved.")