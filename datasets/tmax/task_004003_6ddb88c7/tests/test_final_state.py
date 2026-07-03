# test_final_state.py

import os
import stat
import subprocess
import json
import tempfile
import shutil
import pytest

HOOK_PATH = "/home/user/metrics-dashboard.git/hooks/post-receive"
DATA_DIR = "/home/user/dashboard_data"
LOG_FILE = "/home/user/dashboard_data/push_events.jsonl"
REPO_PATH = "/home/user/metrics-dashboard.git"

def test_hook_exists_and_executable():
    assert os.path.exists(HOOK_PATH), f"Hook not found at {HOOK_PATH}"
    assert os.path.isfile(HOOK_PATH), f"{HOOK_PATH} is not a file"

    st = os.stat(HOOK_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Hook at {HOOK_PATH} is not executable"

def test_hook_invalid_input():
    # Run the hook with invalid input
    process = subprocess.Popen(
        [HOOK_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input="bad data\n")

    assert process.returncode == 1, f"Expected exit code 1 for invalid input, got {process.returncode}"
    assert "Invalid input" in stderr, f"Expected 'Invalid input' in stderr, got: {stderr}"

def test_hook_valid_input():
    # Remove log file if it exists to test creation
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    if os.path.exists(DATA_DIR):
        shutil.rmtree(DATA_DIR)

    old_rev = "0000000000000000000000000000000000000000"
    new_rev = "1111111111111111111111111111111111111111"
    ref = "refs/heads/main"

    process = subprocess.Popen(
        [HOOK_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    process.communicate(input=f"{old_rev} {new_rev} {ref}\n")

    assert process.returncode == 0, f"Expected exit code 0 for valid input, got {process.returncode}"

    assert os.path.isdir(DATA_DIR), f"Directory {DATA_DIR} was not created"
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} was not created"

    # Check permissions
    st = os.stat(LOG_FILE)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o644, f"Expected permissions 644 for {LOG_FILE}, got {oct(perms)}"

    # Check content
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()

    assert len(lines) >= 1, "Log file is empty"
    last_line = lines[-1].strip()

    expected_json = '{"event":"push","ref":"refs/heads/main","new_commit":"1111111111111111111111111111111111111111"}'
    assert last_line == expected_json, f"Expected JSON {expected_json}, got {last_line}"

def test_end_to_end_git_push():
    # Clean up log file
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dir = os.path.join(tmpdir, "test-clone")

        # Clone
        subprocess.run(["git", "clone", REPO_PATH, clone_dir], check=True, capture_output=True)

        # Commit
        test_file = os.path.join(clone_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test\n")

        subprocess.run(["git", "add", "test.txt"], cwd=clone_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clone_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Test commit"], cwd=clone_dir, check=True, capture_output=True)

        # Push
        push_result = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True, text=True)
        assert push_result.returncode == 0, f"Git push failed: {push_result.stderr}"

        # Check log file
        assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} was not created after git push"

        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()

        assert len(lines) >= 1, "Log file is empty after git push"
        last_line = lines[-1].strip()

        try:
            data = json.loads(last_line)
        except json.JSONDecodeError:
            pytest.fail(f"Log line is not valid JSON: {last_line}")

        assert data.get("event") == "push", "event should be 'push'"
        assert data.get("ref") == "refs/heads/master", "ref should be 'refs/heads/master'"
        assert "new_commit" in data, "new_commit missing in JSON"
        assert len(data["new_commit"]) == 40, "new_commit should be a 40-character hash"