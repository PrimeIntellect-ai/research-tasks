# test_final_state.py

import os
import subprocess
import pytest

def test_timeline_log():
    timeline_path = "/home/user/timeline.log"
    assert os.path.isfile(timeline_path), f"{timeline_path} does not exist."

    with open(timeline_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 8, f"Expected 8 lines in {timeline_path}, but found {len(lines)}."

    # Check if lines are sorted by timestamp
    timestamps = [line.split(" ")[0] for line in lines]
    assert timestamps == sorted(timestamps), "Lines in timeline.log are not sorted chronologically."

def test_bad_file_txt():
    bad_file_path = "/home/user/bad_file.txt"
    assert os.path.isfile(bad_file_path), f"{bad_file_path} does not exist."

    with open(bad_file_path, "r") as f:
        content = f.read().strip()

    assert content == "/var/data/critical data.txt", f"Expected bad_file.txt to contain '/var/data/critical data.txt', but got '{content}'."

def test_rust_binary_execution():
    binary_path = "/home/user/state-sync/target/release/state-sync"
    state_file = "/home/user/logs/state.txt"

    assert os.path.isfile(binary_path), f"Rust binary {binary_path} does not exist. Did you run 'cargo build --release'?"
    assert os.access(binary_path, os.X_OK), f"Rust binary {binary_path} is not executable."

    try:
        result = subprocess.run(
            [binary_path, state_file],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The Rust binary timed out. It might still be stuck in an infinite loop.")

    assert result.returncode == 0, f"Expected exit code 0, but got {result.returncode}. Stderr: {result.stderr}"
    assert "Convergence achieved." in result.stdout, "The output did not contain 'Convergence achieved.'"