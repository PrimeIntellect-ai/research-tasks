# test_final_state.py

import os
import subprocess
import tempfile
import pytest

REPO_DIR = "/home/user/uptime_monitor"
BAD_COMMIT_FILE = "/home/user/bad_commit.txt"
FINAL_UPTIME_FILE = "/home/user/final_uptime.txt"

def get_bad_commit_hash():
    """Find the commit that introduced the sum() regression."""
    log_output = subprocess.check_output(
        ["git", "log", "-p"], 
        cwd=REPO_DIR, 
        text=True
    )
    current_commit = None
    for line in log_output.splitlines():
        if line.startswith("commit "):
            current_commit = line.split()[1]
        # The bad commit changed math.fsum to sum
        if line.startswith("-") and "math.fsum" in line:
            # Confirm the addition of sum()
            return current_commit
    return None

def get_expected_uptime():
    """Run the v1.0 version of the script to get the expected uptime."""
    good_script = subprocess.check_output(
        ["git", "show", "v1.0:check_uptime.py"], 
        cwd=REPO_DIR, 
        text=True
    )

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(good_script)
        temp_name = f.name

    try:
        output = subprocess.check_output(
            ["python3", temp_name], 
            cwd=REPO_DIR, 
            text=True
        )
        # The script prints the uptime rounded to 5 decimal places
        return output.strip().splitlines()[-1]
    finally:
        os.remove(temp_name)

def test_bad_commit_identified():
    assert os.path.isfile(BAD_COMMIT_FILE), f"{BAD_COMMIT_FILE} does not exist."

    with open(BAD_COMMIT_FILE, "r") as f:
        student_commit = f.read().strip()

    expected_commit = get_bad_commit_hash()
    assert expected_commit is not None, "Could not find the bad commit in git history (test setup issue)."

    assert student_commit == expected_commit, (
        f"Incorrect bad commit hash. Expected {expected_commit}, got {student_commit}"
    )

def test_final_uptime_calculated():
    assert os.path.isfile(FINAL_UPTIME_FILE), f"{FINAL_UPTIME_FILE} does not exist."

    with open(FINAL_UPTIME_FILE, "r") as f:
        student_uptime = f.read().strip()

    expected_uptime = get_expected_uptime()

    assert student_uptime == expected_uptime, (
        f"Incorrect final uptime. Expected {expected_uptime}, got {student_uptime}"
    )

def test_check_uptime_script_fixed():
    script_path = os.path.join(REPO_DIR, "check_uptime.py")
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # It should not use the built-in sum for delays anymore
    # A proper fix uses math.fsum or similar precision summation
    assert "math.fsum" in content or "fsum" in content, (
        "The script does not appear to use math.fsum for precise floating point summation."
    )

    # The script should run without assertion errors
    try:
        subprocess.check_output(["python3", "check_uptime.py"], cwd=REPO_DIR, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"check_uptime.py failed to run or failed its assertion:\n{e.output}")