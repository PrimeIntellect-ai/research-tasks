# test_final_state.py

import os
import subprocess
import pytest

def test_recovered_multiplier():
    filepath = "/home/user/recovered_multiplier.txt"
    assert os.path.isfile(filepath), f"The file {filepath} was not created."
    with open(filepath, "r") as f:
        content = f.read().strip()
    assert content == "4285", f"Expected recovered multiplier to be '4285', but got '{content}'."

def test_ticket_resolution():
    filepath = "/home/user/ticket_resolution.txt"
    assert os.path.isfile(filepath), f"The file {filepath} was not created."
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {filepath}, but found {len(lines)}."
    assert lines[0] == "4285", f"Expected line 1 to be '4285', but got '{lines[0]}'."
    assert lines[1] == "73", f"Expected line 2 to be '73', but got '{lines[1]}'."

def test_process_killed():
    # Check if sequence_worker.py is still running
    try:
        output = subprocess.check_output(["pgrep", "-f", "sequence_worker.py"], text=True)
        assert output.strip() == "", "The sequence_worker.py process is still running. It should have been killed."
    except subprocess.CalledProcessError:
        # pgrep returns non-zero exit code if no processes are matched, which is expected
        pass