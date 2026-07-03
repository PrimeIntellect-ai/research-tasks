# test_final_state.py

import os
import subprocess
import pytest

def test_highest_indegree():
    file_path = "/home/user/highest_indegree.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read().strip()
    assert content == "vault-primary", f"Expected 'vault-primary' in {file_path}, got '{content}'"

def test_bidirectional():
    file_path = "/home/user/bidirectional.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read().strip()
    assert content == "vault-dr vault-primary", f"Expected 'vault-dr vault-primary' in {file_path}, got '{content}'"

def test_affected_dbs():
    file_path = "/home/user/affected_dbs.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."
    expected = [
        "backup-edge",
        "backup-tier1",
        "backup-tier2",
        "db-analytics",
        "db-edge1",
        "db-edge2",
        "db-legacy",
        "db-main",
        "db-users",
        "vault-primary"
    ]
    with open(file_path, "r") as f:
        content = f.read().splitlines()
    assert content == expected, f"Contents of {file_path} do not match the expected list of affected databases."

def test_find_affected_script_exists_and_executable():
    script_path = "/home/user/find_affected.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_find_affected_script_functionality():
    script_path = "/home/user/find_affected.sh"
    # Run the script with "backup-tier1"
    # Expected: db-main, db-analytics
    result = subprocess.run([script_path, "backup-tier1"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute."
    output = result.stdout.strip().splitlines()
    expected = ["db-analytics", "db-main"]
    assert sorted(output) == expected, f"Script output for 'backup-tier1' did not match expected output."

def test_find_affected_script_cyclic_handling():
    script_path = "/home/user/find_affected.sh"
    # Run the script with "vault-primary"
    # Should handle cycle with vault-dr
    result = subprocess.run([script_path, "vault-primary"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute on cyclic graph."
    output = result.stdout.strip().splitlines()
    expected = [
        "backup-edge",
        "backup-tier1",
        "backup-tier2",
        "db-analytics",
        "db-edge1",
        "db-edge2",
        "db-legacy",
        "db-main",
        "db-users",
        "vault-dr"
    ]
    assert sorted(output) == expected, f"Script output for 'vault-primary' did not match expected output."