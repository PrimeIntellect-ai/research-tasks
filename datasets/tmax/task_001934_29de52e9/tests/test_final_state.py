# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_identified():
    bad_commit_file = "/home/user/bad_commit.txt"
    assert os.path.isfile(bad_commit_file), f"{bad_commit_file} does not exist."

    with open(bad_commit_file, "r") as f:
        student_sha = f.read().strip()

    try:
        expected_sha = subprocess.check_output(
            ["git", "rev-list", "-n", "1", "bad-commit-tag"],
            cwd="/home/user/perf_math",
            universal_newlines=True
        ).strip()
    except subprocess.CalledProcessError:
        pytest.fail("Failed to retrieve the expected bad commit SHA from the git repository.")

    assert student_sha == expected_sha, f"Expected commit SHA {expected_sha}, but got {student_sha}"

def test_correct_sum_calculated():
    correct_sum_file = "/home/user/correct_sum.txt"
    assert os.path.isfile(correct_sum_file), f"{correct_sum_file} does not exist."

    with open(correct_sum_file, "r") as f:
        student_sum_str = f.read().strip()

    assert student_sum_str.isdigit(), f"{correct_sum_file} does not contain a valid integer."
    student_sum = int(student_sum_str)

    # Recompute the expected sum from the chunks
    chunks_dir = "/home/user/perf_math/chunks"
    expected_sum = 0
    for filename in os.listdir(chunks_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(chunks_dir, filename), "r") as f:
                for line in f:
                    val = line.strip()
                    if val:
                        expected_sum += int(val)

    assert student_sum == expected_sum, f"Expected sum {expected_sum}, but got {student_sum}"

def test_fixed_aggregate_script():
    fixed_script = "/home/user/fixed_aggregate.sh"
    assert os.path.isfile(fixed_script), f"{fixed_script} does not exist."
    assert os.access(fixed_script, os.X_OK), f"{fixed_script} is not executable."

    with open(fixed_script, "r") as f:
        content = f.read()

    # Check for locking mechanisms
    has_flock = "flock" in content
    has_mkdir_lock = "mkdir" in content and "lock" in content.lower()
    has_lockfile = "lockfile" in content

    assert has_flock or has_mkdir_lock or has_lockfile, "No safe atomic Bash locking mechanism (like flock) found in the fixed script."

def test_crash_input_triggers_bug():
    crash_file = "/home/user/crash_input.txt"
    assert os.path.isfile(crash_file), f"{crash_file} does not exist."

    with open(crash_file, "r") as f:
        content = f.read()

    numbers = []
    for item in content.split():
        item = item.strip()
        if item:
            assert item.lstrip('-').isdigit(), f"Crash input contains non-integer value: {item}"
            numbers.append(int(item))

    assert len(numbers) > 0, "Crash input file is empty."

    max_val = max(numbers)
    min_val = min(numbers)

    assert max_val == min_val, f"To trigger the divide-by-zero bug, max and min must be equal. Got max={max_val}, min={min_val}."