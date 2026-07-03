# test_final_state.py

import os
import stat
import pytest

def test_tracker_script_exists_and_executable():
    script_path = "/home/user/tracker.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_tracker_script_uses_flock():
    script_path = "/home/user/tracker.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "flock" in content, f"Script {script_path} does not use 'flock' as required."

def test_summary_log_contents():
    log_path = "/home/user/summary.log"
    assert os.path.isfile(log_path), f"Summary log {log_path} was not generated."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "a.bin: 1A2B3C4D",
        "d.bin: F5E6D7C8"
    }

    actual_lines = set(lines)

    assert len(lines) == 2, f"Expected exactly 2 lines in {log_path}, found {len(lines)}."
    assert actual_lines == expected_lines, f"Contents of {log_path} do not match the expected output. Expected {expected_lines}, but got {actual_lines}."