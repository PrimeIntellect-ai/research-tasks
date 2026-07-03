# test_final_state.py

import os
import json
import subprocess
import pytest

def test_solution_json_exists():
    assert os.path.isfile("/home/user/solution.json"), "/home/user/solution.json does not exist."

def test_solution_json_content():
    with open("/home/user/solution.json", "r") as f:
        try:
            solution = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/solution.json is not valid JSON.")

    assert "bad_commit_hash" in solution, "Missing 'bad_commit_hash' in solution.json."
    assert "leaking_line_content" in solution, "Missing 'leaking_line_content' in solution.json."
    assert "fixed_successfully" in solution, "Missing 'fixed_successfully' in solution.json."

    with open("/home/user/.truth_bad_commit", "r") as f:
        expected_bad_commit = f.read().strip()

    assert solution["bad_commit_hash"] == expected_bad_commit, f"Incorrect bad_commit_hash. Expected {expected_bad_commit}."

    expected_line = "WARN: [ID:999] CORRUPTED_ENTRY parse_failure_0x88"
    assert solution["leaking_line_content"] == expected_line, f"Incorrect leaking_line_content. Expected '{expected_line}'."
    assert solution["fixed_successfully"] is True, "'fixed_successfully' should be true."

def test_leak_fixed():
    # Run test_leak.py against suspicious_logs.txt
    try:
        result = subprocess.run(
            ["python3", "/home/user/log_service/test_leak.py", "/home/user/suspicious_logs.txt"],
            capture_output=True,
            text=True,
            cwd="/home/user/log_service"
        )
    except Exception as e:
        pytest.fail(f"Failed to execute test_leak.py: {e}")

    assert result.returncode == 0, f"test_leak.py exited with code {result.returncode}, meaning the leak is not fixed. Output: {result.stdout} {result.stderr}"

def test_pyyaml_dependency_fixed():
    try:
        result = subprocess.run(
            ["pip", "show", "pyyaml"],
            capture_output=True,
            text=True,
            check=True
        )
        assert "Version: 6.0" in result.stdout, "PyYAML version 6.0 is not installed. Dependency issue not resolved."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run pip show pyyaml")