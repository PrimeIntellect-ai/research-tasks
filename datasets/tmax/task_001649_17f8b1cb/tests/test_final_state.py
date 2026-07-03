# test_final_state.py

import os
import subprocess
import pytest

def test_bug_commit_txt_matches_expected():
    bug_commit_path = "/home/user/bug_commit.txt"
    expected_commit_path = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(bug_commit_path), f"{bug_commit_path} is missing."
    assert os.path.isfile(expected_commit_path), f"{expected_commit_path} is missing."

    with open(bug_commit_path, "r") as f:
        actual_commit = f.read().strip()

    with open(expected_commit_path, "r") as f:
        expected_commit = f.read().strip()

    assert actual_commit == expected_commit, (
        f"Incorrect commit hash in {bug_commit_path}. "
        f"Expected '{expected_commit}', but got '{actual_commit}'."
    )

def test_test_sh_runs_successfully():
    test_sh_path = "/home/user/job_queue/test.sh"
    assert os.path.isfile(test_sh_path), f"{test_sh_path} is missing."

    try:
        result = subprocess.run(
            ["./test.sh"],
            cwd="/home/user/job_queue",
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0, (
            f"./test.sh failed with exit code {result.returncode}.\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    except subprocess.TimeoutExpired:
        pytest.fail("./test.sh timed out. The deadlock bug is likely still present.")
    except Exception as e:
        pytest.fail(f"Failed to execute ./test.sh: {e}")

def test_queue_c_bug_removed():
    queue_c_path = "/home/user/job_queue/queue.c"
    assert os.path.isfile(queue_c_path), f"{queue_c_path} is missing."

    with open(queue_c_path, "r") as f:
        content = f.read()

    # The bug introduced was exactly this string
    buggy_statement = "i = (i + 1) % (MAX_JOBS + 1);"

    assert buggy_statement not in content, (
        f"{queue_c_path} still contains the off-by-one modulo error: '{buggy_statement}'"
    )