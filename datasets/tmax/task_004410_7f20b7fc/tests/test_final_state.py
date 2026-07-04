# test_final_state.py

import os
import subprocess
import pytest
import tempfile

REPO_DIR = "/home/user/data_processor"
SCRIPT_PATH = os.path.join(REPO_DIR, "process_logs.sh")
HANGING_INPUT_FILE = "/home/user/hanging_input.txt"
BAD_COMMIT_FILE = "/home/user/bad_commit.txt"

def test_hanging_input_file():
    assert os.path.isfile(HANGING_INPUT_FILE), f"{HANGING_INPUT_FILE} does not exist."
    with open(HANGING_INPUT_FILE, "r") as f:
        content = f.read().strip()
    assert content == "1337", f"Expected hanging input to be '1337', got '{content}'."

def test_bad_commit_file():
    assert os.path.isfile(BAD_COMMIT_FILE), f"{BAD_COMMIT_FILE} does not exist."
    with open(BAD_COMMIT_FILE, "r") as f:
        student_commit = f.read().strip()

    # Get the actual bad commit hash from git history
    try:
        result = subprocess.run(
            ["git", "log", "--grep=Refactor to handle specific codes", "--format=%H"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        expected_commit = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to find expected bad commit in git history: {e.stderr}")

    assert expected_commit, "Could not determine the expected bad commit hash."
    assert student_commit == expected_commit, f"Expected bad commit hash {expected_commit}, got {student_commit}."

def test_script_fixed_and_correct():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

    # Test with 1337 and another number
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        tmp.write("1337\n100\n")
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [SCRIPT_PATH, tmp_path],
            capture_output=True,
            text=True,
            timeout=2  # Should not hang
        )
        assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"
        output = result.stdout.strip()
        assert output == "1437", f"Expected script output '1437', got '{output}'."
    except subprocess.TimeoutExpired:
        pytest.fail("The script timed out (hanged) on the input, meaning the infinite loop bug is not fixed.")
    finally:
        os.remove(tmp_path)

def test_latest_commit_message():
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%B"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        commit_msg = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to get latest commit message: {e.stderr}")

    assert commit_msg == "Fix infinite loop", f"Expected commit message 'Fix infinite loop', got '{commit_msg}'."