# test_final_state.py

import os
import pytest

def test_solution_file_contains_correct_value():
    pcap_file = "/home/user/pcap_summary.log"
    solution_file = "/home/user/solution.txt"

    assert os.path.isfile(pcap_file), f"Missing file: {pcap_file}"
    assert os.path.isfile(solution_file), f"Missing solution file: {solution_file}"

    expected_total = 0
    with open(pcap_file, 'r') as f:
        lines = f.read().strip().split('\n')

    for line in lines:
        parts = line.split()
        if not parts or parts[0] == "session_id":
            continue

        try:
            bytes_transferred = int(parts[1])
            start_time = int(parts[2])
            end_time = int(parts[3])
        except ValueError:
            continue

        duration = end_time - start_time
        if duration == 0:
            duration = 1

        throughput = bytes_transferred // duration
        expected_total += throughput

    with open(solution_file, 'r') as f:
        solution_content = f.read().strip()

    assert solution_content == str(expected_total), (
        f"Expected solution to be {expected_total}, but found '{solution_content}'"
    )

def test_script_is_executable():
    script_path = "/home/user/network_analyzer.sh"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"