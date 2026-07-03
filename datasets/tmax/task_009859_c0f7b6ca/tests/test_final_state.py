# test_final_state.py
import os
import pytest

def test_profiler_executable_exists():
    path = "/home/user/profiler"
    assert os.path.isfile(path), f"Executable {path} is missing. Did you compile the C file?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_evaluate_script_exists():
    path = "/home/user/evaluate.sh"
    assert os.path.isfile(path), f"Script {path} is missing."
    # While it's best practice to make it executable, we strictly check if it exists.
    # We will check if it's executable just in case, but won't fail if it was run via `bash evaluate.sh`.
    # Actually, the prompt says "Write a Bash script at /home/user/evaluate.sh", so we just check existence.

def test_summary_log_contents():
    path = "/home/user/summary.log"
    assert os.path.isfile(path), f"Report {path} is missing. Did you run the evaluate.sh script?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Mean 1-thread: 10.00",
        "Mean 8-thread: 2.00",
        "Speedup: 5.00",
        "Hypothesis Met: YES"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == 4, f"Expected 4 lines in {path}, found {len(actual_lines)}."

    for i, expected in enumerate(expected_lines):
        assert actual_lines[i] == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual_lines[i]}'."