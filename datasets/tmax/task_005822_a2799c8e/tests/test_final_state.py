# test_final_state.py

import os
import re
import subprocess

def test_source_code_exists():
    src_path = "/home/user/hook.cpp"
    assert os.path.isfile(src_path), f"C++ source code file not found at {src_path}."

def test_hook_executable():
    hook_path = "/home/user/finops-repo/.git/hooks/post-commit"
    assert os.path.isfile(hook_path), f"Git hook not found at {hook_path}."
    assert os.access(hook_path, os.X_OK), f"Git hook at {hook_path} is not executable."

def test_log_file_exists():
    log_path = "/home/user/cost_health.log"
    assert os.path.isfile(log_path), f"Log file not found at {log_path}."

def test_log_content_and_format():
    log_path = "/home/user/cost_health.log"
    repo_path = "/home/user/finops-repo"

    # Get the latest commit hash
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        latest_commit = result.stdout.strip()
    except subprocess.CalledProcessError:
        assert False, "Failed to retrieve the latest Git commit hash. Did you make a commit?"

    assert len(latest_commit) == 40, "Invalid commit hash retrieved."

    with open(log_path, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"Log file {log_path} is empty."

    last_line = lines[-1]

    # Expected format: [YYYY-MM-DD HH:MM:SS JST] COMMIT: <hash> - BILLING_SVC: UP
    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} JST\] COMMIT: ([a-f0-9]{40}) - BILLING_SVC: (UP|DOWN)$"
    match = re.match(pattern, last_line)

    assert match is not None, f"Log line format is incorrect. Found: '{last_line}'"

    logged_hash = match.group(1)
    logged_state = match.group(2)

    assert logged_hash == latest_commit, f"Commit hash in log ({logged_hash}) does not match the latest commit ({latest_commit})."
    assert logged_state == "UP", f"Expected BILLING_SVC to be UP, but found {logged_state}."