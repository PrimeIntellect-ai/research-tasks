# test_final_state.py

import os
import re
import subprocess
import pytest

def get_bad_commit_hash():
    repo_path = "/home/user/repo"
    try:
        log_output = subprocess.check_output(
            ["git", "log", "--format=%H %s"],
            cwd=repo_path,
            text=True
        )
        for line in log_output.strip().split("\n"):
            if "Refactor calculation logic" in line:
                return line.split()[0]
    except subprocess.CalledProcessError:
        pass
    return None

def test_resolution_file_exists():
    assert os.path.isfile("/home/user/resolution.txt"), "The file /home/user/resolution.txt does not exist."

def test_resolution_file_contents():
    resolution_path = "/home/user/resolution.txt"
    with open(resolution_path, "r") as f:
        content = f.read()

    # Parse contents
    req_match = re.search(r"First failing REQ:\s*(.+)", content)
    inputs_match = re.search(r"Failing inputs:\s*(.+)", content)
    commit_match = re.search(r"Overflow commit:\s*(.+)", content)
    constant_match = re.search(r"Oracle XOR constant:\s*(.+)", content)
    output_match = re.search(r"Fixed program output for failing inputs:\s*(.+)", content)

    assert req_match, "Could not find 'First failing REQ' in resolution.txt"
    assert req_match.group(1).strip() == "REQ-1003", "Incorrect first failing REQ"

    assert inputs_match, "Could not find 'Failing inputs' in resolution.txt"
    assert inputs_match.group(1).strip() == "x=85000 y=92000", "Incorrect failing inputs"

    bad_commit = get_bad_commit_hash()
    assert bad_commit is not None, "Could not find the bad commit in git history"

    assert commit_match, "Could not find 'Overflow commit' in resolution.txt"
    assert commit_match.group(1).strip() == bad_commit, "Incorrect overflow commit hash"

    assert constant_match, "Could not find 'Oracle XOR constant' in resolution.txt"
    assert constant_match.group(1).strip().upper() == "0XCAFEBABE", "Incorrect Oracle XOR constant"

    assert output_match, "Could not find 'Fixed program output for failing inputs' in resolution.txt"
    assert output_match.group(1).strip() == "4712030654", "Incorrect fixed program output"

def test_fixed_calc_program():
    calc_bin = "/home/user/repo/calc"
    assert os.path.isfile(calc_bin), "The compiled binary /home/user/repo/calc does not exist."
    assert os.access(calc_bin, os.X_OK), "The file /home/user/repo/calc is not executable."

    try:
        output = subprocess.check_output([calc_bin, "85000", "92000"], text=True).strip()
        assert output == "4712030654", f"The compiled binary produced incorrect output: {output} instead of 4712030654"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run the compiled binary: {e}")