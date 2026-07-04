# test_final_state.py

import os
import csv
import stat
import pytest

def compute_expected_changes(input_csv_path):
    """
    Derives the expected changes.csv output by simulating the tracking logic
    on the actual configs.csv file.
    """
    with open(input_csv_path, 'r') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            return ""

        config_keys = headers[2:]

        last_state = {}
        changes = {}

        for row in reader:
            if not row or len(row) < 2:
                continue
            server_id = row[1].upper()
            if server_id not in last_state:
                last_state[server_id] = {}
                changes[server_id] = {k: 0 for k in config_keys}

            for i, key in enumerate(config_keys):
                if 2 + i < len(row):
                    val = row[2 + i]
                    if key in last_state[server_id]:
                        if last_state[server_id][key] != val:
                            changes[server_id][key] += 1
                    last_state[server_id][key] = val

    result = []
    for server_id in sorted(changes.keys()):
        for key in sorted(config_keys):
            result.append(f"{server_id},{key},{changes[server_id][key]}")

    return "\n".join(result) + "\n"

def test_tracker_c_exists():
    file_path = "/home/user/tracker.c"
    assert os.path.isfile(file_path), f"Source file {file_path} is missing."

def test_tracker_executable_exists():
    file_path = "/home/user/tracker"
    assert os.path.isfile(file_path), f"Executable {file_path} is missing."
    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{file_path} is not executable."

def test_changes_csv_matches_expected():
    input_path = "/home/user/configs.csv"
    output_path = "/home/user/changes.csv"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    expected_csv_content = compute_expected_changes(input_path)

    with open(output_path, "r") as f:
        actual_content = f.read()

    # Compare line by line to give a clean error message
    expected_lines = [line for line in expected_csv_content.strip().split("\n") if line]
    actual_lines = [line for line in actual_content.strip().split("\n") if line]

    assert actual_lines == expected_lines, (
        f"Output in {output_path} does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )