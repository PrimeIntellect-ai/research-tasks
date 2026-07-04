# test_final_state.py

import os
import stat

def test_executable_exists():
    """Check that the compiled program /home/user/audit exists and is executable."""
    executable_path = "/home/user/audit"
    assert os.path.exists(executable_path), f"{executable_path} does not exist. Did you compile the C program?"
    assert os.path.isfile(executable_path), f"{executable_path} is not a file."

    # Check if executable
    st = os.stat(executable_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"{executable_path} is not executable."

def test_violations_file_exists():
    """Check that the violations.txt file was created."""
    violations_path = "/home/user/violations.txt"
    assert os.path.exists(violations_path), f"{violations_path} does not exist. Did you run the program and save the output?"
    assert os.path.isfile(violations_path), f"{violations_path} is not a regular file."

def test_violations_correctness():
    """Check that violations.txt contains the correct, sorted violations derived from the CSV files."""
    logs_path = "/home/user/logs.csv"
    perms_path = "/home/user/perms.csv"
    violations_path = "/home/user/violations.txt"

    # Derive expected violations dynamically
    logs = []
    if os.path.exists(logs_path):
        with open(logs_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    logs.append(line.split(","))

    perms = {}
    if os.path.exists(perms_path):
        with open(perms_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) >= 3:
                        perms[(parts[0], parts[1])] = int(parts[2])

    expected_violations = []
    for user_id, resource_id in logs:
        granted = perms.get((user_id, resource_id), 0)
        if granted == 0:
            expected_violations.append(f"{user_id},{resource_id}")

    expected_violations.sort()

    # Read actual violations
    actual_violations = []
    with open(violations_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                actual_violations.append(line)

    assert actual_violations == expected_violations, (
        f"Contents of {violations_path} do not match the expected sorted violations.\n"
        f"Expected: {expected_violations}\n"
        f"Actual: {actual_violations}"
    )