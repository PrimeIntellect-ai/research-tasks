# test_final_state.py
import os
import json
import subprocess
import pytest

def test_rust_compiles():
    """Verify the Rust project compiles successfully."""
    project_dir = "/home/user/math_ws_server"
    assert os.path.isdir(project_dir), f"Project directory {project_dir} does not exist."

    result = subprocess.run(
        ["cargo", "check"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Rust project failed to compile:\n{result.stderr}"

def test_ws_output_log():
    """Verify the output log contains the correct JSON responses."""
    log_path = "/home/user/ws_output.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines of output in {log_path}, found {len(lines)}."

    expected_outputs = [
        [[0, 5], [3, 4], [4, 3], [5, 0]],
        [[1, 8], [4, 7], [7, 4], [8, 1]],
        [[4, 33], [9, 32], [12, 31], [23, 24], [24, 23], [31, 12], [32, 9], [33, 4]]
    ]

    try:
        parsed_lines = [json.loads(line) for line in lines]
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON from {log_path}: {e}")

    for i, (actual, expected) in enumerate(zip(parsed_lines, expected_outputs)):
        assert actual == expected, f"Mismatch on line {i+1}. Expected {expected}, got {actual}"