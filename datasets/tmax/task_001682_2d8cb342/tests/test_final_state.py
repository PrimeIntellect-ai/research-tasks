# test_final_state.py

import os
import subprocess
import pytest

def test_solution_file():
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"Solution file {solution_path} does not exist."

    with open(solution_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {solution_path}, found {len(lines)}."

    assert lines[0] == "Crashing Line: 6834", f"First line is incorrect. Expected 'Crashing Line: 6834', got '{lines[0]}'"
    assert lines[1] == "Token: parsed_9999_valid_lines", f"Second line is incorrect. Expected 'Token: parsed_9999_valid_lines', got '{lines[1]}'"

def test_binary_fixed():
    binary_path = "/home/user/log_processor"
    log_path = "/home/user/app_logs.txt"

    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

    # Run the binary on the log file
    try:
        result = subprocess.run(
            [binary_path, log_path],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The log_processor binary timed out. It might be stuck in an infinite loop.")

    assert result.returncode == 0, f"The log_processor binary crashed or returned non-zero exit code: {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()
    assert "SUCCESS_TOKEN: parsed_9999_valid_lines" in output, f"The binary did not print the expected success token. Output: {output}"