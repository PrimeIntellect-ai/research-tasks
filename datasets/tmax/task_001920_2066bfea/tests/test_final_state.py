# test_final_state.py

import os
import subprocess

def test_leak_commit_recorded():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/leak_commit.txt"

    assert os.path.isfile(actual_file), f"File {actual_file} does not exist."
    assert os.path.isfile(expected_file), f"Truth file {expected_file} is missing."

    with open(expected_file, "r") as f:
        expected_commit = f.read().strip()

    with open(actual_file, "r") as f:
        actual_commit = f.read().strip()

    assert actual_commit == expected_commit, f"Expected bad commit {expected_commit}, but got {actual_commit}."

def test_daemon_script_fixed():
    script_path = "/home/user/app/daemon.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "-eq -1" not in content, "The bug (-eq -1) is still present in daemon.sh."
    assert "ITEMS=()" in content, "The array clearing logic (ITEMS=()) is missing from daemon.sh."

def test_daemon_script_behavior():
    script_path = "/home/user/app/daemon.sh"
    # Source the script, run process_data, and print the size of ITEMS
    bash_command = f"source {script_path} && process_data && echo ${{#ITEMS[@]}}"

    result = subprocess.run(
        ["bash", "-c", bash_command],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Failed to execute daemon.sh: {result.stderr}"

    output = result.stdout.strip()
    try:
        items_size = int(output)
    except ValueError:
        assert False, f"Expected integer output for ITEMS size, got: {output}"

    assert items_size == 0, f"Memory leak is not fixed. Expected ITEMS size to be 0 after process_data, got {items_size}."

def test_git_branch_is_main():
    repo_path = "/home/user/app"
    result = subprocess.run(
        ["git", "-C", repo_path, "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, "Failed to check git branch."
    branch = result.stdout.strip()
    assert branch in ["main", "master"], f"Expected to be on main branch, but currently on {branch}."