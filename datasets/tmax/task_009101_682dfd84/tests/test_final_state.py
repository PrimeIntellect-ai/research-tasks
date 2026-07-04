# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_txt():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit.txt"

    assert os.path.exists(actual_file), f"{actual_file} does not exist."
    assert os.path.exists(expected_file), f"Truth file {expected_file} is missing."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected bad commit hash {expected_hash}, but got {actual_hash}."

def test_anomalous_line_txt():
    actual_file = "/home/user/anomalous_line.txt"
    assert os.path.exists(actual_file), f"{actual_file} does not exist."

    with open(actual_file, "r") as f:
        actual_line = f.read().strip()

    assert actual_line == "4232", f"Expected anomalous line to be 4232, but got {actual_line}."

def test_main_c_fixes():
    main_c_path = "/home/user/forensics_task/main.c"
    assert os.path.exists(main_c_path), f"{main_c_path} does not exist."

    with open(main_c_path, "r") as f:
        content = f.read()

    # Check for quoting fix
    has_quotes = "\\\"%s\\\"" in content or "'%s'" in content or "\\\"%s/data.csv\\\"" in content
    assert has_quotes, "Could not find quoted path (e.g., \\\"%s\\\") in main.c popen/sprintf command."

    # Check for bounds check
    has_bounds_check = "100" in content and (">" in content or "<" in content)
    assert has_bounds_check, "Could not find bounds checking logic (e.g., val < 100) in main.c."

def test_process_sh_execution():
    # If the user fixed the C program properly, compiling and running it should succeed without segfault.
    base_dir = "/home/user/forensics_task"

    # Recompile to be sure
    subprocess.run(["make"], cwd=base_dir, check=False, capture_output=True)

    # Run process.sh
    result = subprocess.run(["./process.sh"], cwd=base_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"process.sh failed with return code {result.returncode}. Stderr: {result.stderr}"
    assert "Processing complete." in result.stdout, "Script did not output 'Processing complete.'."

def test_final_output_txt():
    actual_file = "/home/user/final_output.txt"
    assert os.path.exists(actual_file), f"{actual_file} does not exist."

    with open(actual_file, "r") as f:
        content = f.read().strip()

    assert "Processing complete." in content, "final_output.txt does not contain 'Processing complete.'."