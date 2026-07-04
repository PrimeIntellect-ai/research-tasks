# test_final_state.py

import os
import subprocess
import pytest

def test_ticket_resolution_content():
    resolution_file = "/home/user/ticket_resolution.txt"
    assert os.path.isfile(resolution_file), f"{resolution_file} is missing"

    expected_bad_commit_file = "/tmp/expected_bad_commit.txt"
    assert os.path.isfile(expected_bad_commit_file), f"{expected_bad_commit_file} is missing"

    with open(expected_bad_commit_file, "r") as f:
        expected_bad_commit = f.read().strip()

    with open(resolution_file, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) >= 2, f"{resolution_file} does not have enough lines"

    expected_line1 = f"Bad Commit: {expected_bad_commit}"
    expected_line2 = "Error Code: ERR_CODE_FP_CANCELLATION_9921"

    assert content[0].strip() == expected_line1, f"First line of {resolution_file} is incorrect. Expected: {expected_line1}"
    assert content[1].strip() == expected_line2, f"Second line of {resolution_file} is incorrect. Expected: {expected_line2}"

def test_simulate_script_fixed():
    dump_file = "/home/user/sim_repo/sim_memory.dmp"
    if os.path.exists(dump_file):
        os.remove(dump_file)

    result = subprocess.run(
        ["python3", "simulate.py"],
        cwd="/home/user/sim_repo",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"simulate.py failed to run. Stderr: {result.stderr}"
    assert "Simulation success" in result.stdout, "simulate.py did not print 'Simulation success'"
    assert not os.path.exists(dump_file), "sim_memory.dmp was generated, indicating a crash occurred"