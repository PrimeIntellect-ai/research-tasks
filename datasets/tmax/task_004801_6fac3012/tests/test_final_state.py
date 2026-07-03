# test_final_state.py

import os
import pytest

def test_raw_fs_file():
    """Check that raw_fs.txt exists and has the correct content."""
    path = "/home/user/raw_fs.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "1672531200 /var/log 5048392", f"Content of {path} is incorrect: {content}"

def test_binaries_exist_and_executable():
    """Check that the staged binaries exist and are executable."""
    blue_bin = "/home/user/deploy_blue/agent_bin"
    green_bin = "/home/user/deploy_green/agent_bin"

    assert os.path.exists(blue_bin), f"Binary {blue_bin} does not exist."
    assert os.access(blue_bin, os.X_OK), f"Binary {blue_bin} is not executable."

    assert os.path.exists(green_bin), f"Binary {green_bin} does not exist."
    assert os.access(green_bin, os.X_OK), f"Binary {green_bin} is not executable."

def test_observability_log():
    """Check that observability.log has the exact expected content."""
    path = "/home/user/observability.log"
    assert os.path.exists(path), f"Log file {path} does not exist."

    expected_lines = [
        "Connectivity OK",
        "[2023/01/01 09:00:00] Mount: /var/log | Free: 5048392 bytes | Env: tuning_stage"
    ]

    with open(path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 2, f"Expected 2 lines in {path}, found {len(lines)}."
    assert lines[0] == expected_lines[0], f"First line of {path} is incorrect. Expected '{expected_lines[0]}', got '{lines[0]}'."
    assert lines[1] == expected_lines[1], f"Second line of {path} is incorrect. Expected '{expected_lines[1]}', got '{lines[1]}'."