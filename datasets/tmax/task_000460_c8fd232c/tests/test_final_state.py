# test_final_state.py

import os
import subprocess
import time
import pytest

def test_analysis_file_contents():
    """Test that analysis.txt contains the correct findings."""
    analysis_file = "/home/user/analysis.txt"
    assert os.path.isfile(analysis_file), f"Analysis file missing: {analysis_file}"

    with open(analysis_file, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) >= 3, f"Expected at least 3 lines in {analysis_file}, found {len(lines)}"

    # Line 1: PID with most records (Worker B -> 2088)
    assert lines[0] == "2088", f"Line 1 should be '2088', got '{lines[0]}'"

    # Line 2: Duplicated record ID
    assert lines[1] == "REQ-0077", f"Line 2 should be 'REQ-0077', got '{lines[1]}'"

    # Line 3: Bottleneck record ID
    assert lines[2] == "REQ-0042", f"Line 3 should be 'REQ-0042', got '{lines[2]}'"

def test_fixed_worker_script_exists_and_executable():
    """Test that fixed_worker.sh exists and is executable."""
    script_file = "/home/user/fixed_worker.sh"
    assert os.path.isfile(script_file), f"Fixed worker script missing: {script_file}"
    assert os.access(script_file, os.X_OK), f"Fixed worker script is not executable: {script_file}"

def test_fixed_worker_concurrency():
    """Test that fixed_worker.sh processes records safely with multiple concurrent instances."""
    script_file = "/home/user/fixed_worker.sh"
    queue_file = "/home/user/data/queue.txt"
    completed_file = "/home/user/data/completed.txt"

    # Recreate the queue file with 100 records
    with open(queue_file, "w") as f:
        for i in range(1, 101):
            f.write(f"REQ-{i:04d}\n")

    # Clear completed.txt if it exists
    if os.path.exists(completed_file):
        os.remove(completed_file)

    # Launch 5 concurrent instances
    processes = []
    for _ in range(5):
        p = subprocess.Popen([script_file])
        processes.append(p)

    # Wait for all processes to complete
    for p in processes:
        p.wait()

    # Verify completed.txt
    assert os.path.isfile(completed_file), f"Completed file missing: {completed_file}"

    with open(completed_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 100, f"Expected exactly 100 lines in {completed_file}, got {len(lines)}"

    unique_lines = set(lines)
    assert len(unique_lines) == 100, f"Expected 100 unique lines, but found duplicates. Unique count: {len(unique_lines)}"

    # Verify format of the output
    for i in range(1, 101):
        expected_line = f"REQ-{i:04d} processed"
        assert expected_line in unique_lines, f"Missing expected output: '{expected_line}'"