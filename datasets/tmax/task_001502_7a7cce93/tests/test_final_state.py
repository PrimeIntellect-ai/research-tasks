# test_final_state.py
import os
import subprocess

def test_bad_commit_identified_correctly():
    bad_commit_path = "/home/user/bad_commit.txt"
    expected_commit_path = "/tmp/.expected_bad_commit"

    assert os.path.isfile(bad_commit_path), f"File {bad_commit_path} does not exist. Did you save the bad commit hash?"
    assert os.path.isfile(expected_commit_path), f"Truth file {expected_commit_path} is missing."

    with open(bad_commit_path, "r") as f:
        actual_commit = f.read().strip()

    with open(expected_commit_path, "r") as f:
        expected_commit = f.read().strip()

    assert actual_commit == expected_commit, f"The commit hash in {bad_commit_path} is incorrect."

def test_test_monitor_not_modified():
    repo_dir = "/home/user/uptime_monitor"

    # Ensure test_monitor.py hasn't been modified compared to the v1.0 tag
    result = subprocess.run(
        ["git", "show", "v1.0:test_monitor.py"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=True
    )
    expected_content = result.stdout.strip()

    with open(os.path.join(repo_dir, "test_monitor.py"), "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, "test_monitor.py was modified. You must fix monitor.py without changing the tests."

def test_monitor_tests_pass():
    repo_dir = "/home/user/uptime_monitor"

    result = subprocess.run(
        ["python3", "test_monitor.py"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Tests in test_monitor.py are still failing or have errors:\n{result.stderr}\n{result.stdout}"