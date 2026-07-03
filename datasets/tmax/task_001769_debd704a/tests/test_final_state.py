# test_final_state.py
import os
import pytest

def test_unified_index_log_exists():
    path = "/home/user/unified_index.log"
    assert os.path.isfile(path), f"File {path} does not exist. The script must create this file."

def test_unified_index_log_contents():
    path = "/home/user/unified_index.log"
    assert os.path.isfile(path), f"File {path} does not exist."

    expected_lines = {
        "team_alpha.tar.gz::docs/api.md -> 3",
        "team_alpha.tar.gz::legacy.zip/v1.md -> 5",
        "team_beta.zip::readme.md -> 2",
        "team_gamma.stream.gz::team_gamma.stream -> 4"
    }

    with open(path, "r") as f:
        actual_lines = set(line.strip() for line in f if line.strip())

    missing = expected_lines - actual_lines
    unexpected = actual_lines - expected_lines

    error_msg = []
    if missing:
        error_msg.append(f"Missing expected lines: {missing}")
    if unexpected:
        error_msg.append(f"Unexpected lines found: {unexpected}")

    assert not missing and not unexpected, " | ".join(error_msg)