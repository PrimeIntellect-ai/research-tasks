# test_final_state.py
import os

def test_investigation_file():
    investigation_file = "/home/user/investigation.txt"
    expected_commit_file = "/tmp/expected_commit.txt"

    assert os.path.isfile(investigation_file), f"File {investigation_file} does not exist."
    assert os.path.isfile(expected_commit_file), f"Truth file {expected_commit_file} is missing."

    with open(investigation_file, "r") as f:
        lines = [line.strip() for line in f.read().splitlines()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {investigation_file}, found {len(lines)}."

    assert lines[0] == "773", f"Line 1 should be '773', got '{lines[0]}'."
    assert lines[1] == "/tmp/.backdoor_x82", f"Line 2 should be '/tmp/.backdoor_x82', got '{lines[1]}'."

    with open(expected_commit_file, "r") as f:
        expected_commit = f.read().strip()

    assert lines[2] == expected_commit, f"Line 3 should be '{expected_commit}', got '{lines[2]}'."