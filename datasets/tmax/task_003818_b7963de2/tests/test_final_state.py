# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/event_service"
FINAL_STATE_FILE = "/home/user/final_state.txt"
BACKLOG_FILE = os.path.join(WORKSPACE_DIR, "backlog.txt")

def compute_expected_sums(backlog_path):
    """
    Simulates the C++ ring buffer logic to derive the possible expected sums.
    There are two common ways to fix the negative modulo bug in C++:
    1. index = abs(id) % 10
    2. index = (id % 10 + 10) % 10
    Depending on the fix used, the final sum might differ due to index collisions.
    """
    if not os.path.isfile(backlog_path):
        return []

    # Method 1: abs(id) % 10
    buffer_abs = [0] * 10
    # Method 2: (id % 10 + 10) % 10 (which is Python's default % behavior)
    buffer_mod = [0] * 10

    with open(backlog_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                event_id = int(parts[0])
                val = int(parts[1])

                # C++ abs behavior
                idx_abs = abs(event_id) % 10
                buffer_abs[idx_abs] = val

                # C++ wrap-around behavior (Python's default modulo handles negative properly)
                idx_mod = event_id % 10
                buffer_mod[idx_mod] = val

    return [sum(buffer_abs), sum(buffer_mod)]

def test_make_compiles_cleanly():
    """Verify that 'make' runs successfully in the workspace."""
    assert os.path.isdir(WORKSPACE_DIR), f"Workspace directory {WORKSPACE_DIR} is missing."

    result = subprocess.run(
        ["make"],
        cwd=WORKSPACE_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'make' failed to compile cleanly.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_make_test_runs_successfully():
    """Verify that 'make test' compiles and runs the regression test successfully."""
    result = subprocess.run(
        ["make", "test"],
        cwd=WORKSPACE_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'make test' failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_final_state_output():
    """Verify that final_state.txt contains the correct final sum."""
    assert os.path.isfile(FINAL_STATE_FILE), f"Final output file {FINAL_STATE_FILE} is missing."

    with open(FINAL_STATE_FILE, "r") as f:
        content = f.read().strip()

    expected_sums = compute_expected_sums(BACKLOG_FILE)
    assert expected_sums, "Could not compute expected sums (backlog.txt might be missing or empty)."

    valid_outputs = [f"Final Sum: {s}" for s in expected_sums]

    assert content in valid_outputs, (
        f"Contents of {FINAL_STATE_FILE} ('{content}') do not match any expected outputs: {valid_outputs}. "
        "Check your modulo fix logic."
    )