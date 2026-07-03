# test_final_state.py
import os
import stat
import subprocess
import tempfile
import pytest

def get_default_interface():
    res = subprocess.run(["ip", "route"], capture_output=True, text=True)
    for line in res.stdout.splitlines():
        if line.startswith("default"):
            parts = line.split()
            if "dev" in parts:
                idx = parts.index("dev")
                return parts[idx + 1]
    return None

def test_git_hook_exists_and_executable():
    hook_path = "/home/user/monitor.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"Git hook at {hook_path} is not executable"

def test_alert_script_exists():
    script_path = "/home/user/alert_check.py"
    assert os.path.isfile(script_path), f"Alert script not found at {script_path}"

def test_alert_logging():
    repo_url = "/home/user/monitor.git"

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dir = os.path.join(tmpdir, "monitor_clone")

        # Clone the repository
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True, capture_output=True)

        # Configure git
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=clone_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clone_dir, check=True)

        # Create an off-hours commit
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = "1704117600 +0000"
        env["GIT_COMMITTER_DATE"] = "1704117600 +0000"

        subprocess.run(["git", "commit", "--allow-empty", "-m", "Off-hours commit"], 
                       cwd=clone_dir, env=env, check=True, capture_output=True)

        # Get the new commit hash
        res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=clone_dir, check=True, capture_output=True, text=True)
        new_rev = res.stdout.strip()

        # Push the commit
        subprocess.run(["git", "push", "origin", "main"], cwd=clone_dir, check=True, capture_output=True)

    # Check alerts.log
    log_path = "/home/user/alerts.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    # Check permissions
    st = os.stat(log_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Permissions for {log_path} are {oct(perms)}, expected 0o600."

    # Check log content
    iface = get_default_interface()
    assert iface is not None, "Could not determine default network interface."

    expected_log = f"ALERT: commit={new_rev} tz_hour=23 iface={iface}"

    with open(log_path, "r") as f:
        log_contents = f.read()

    assert expected_log in log_contents, f"Expected log entry '{expected_log}' not found in {log_path}. Found:\n{log_contents}"