# test_final_state.py
import os
import subprocess
import pytest

def test_db_sqlite_exists():
    path = '/home/user/restored_apps/db.sqlite'
    assert os.path.isfile(path), f"File {path} does not exist. App2 requires this to pass health checks."

def test_manage_services_script():
    script_path = '/home/user/manage_services.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    # Run the script with the 'status' argument
    # We use bash explicitly in case it's missing a shebang, but it should be executable.
    result = subprocess.run(['bash', script_path, 'status'], capture_output=True)
    assert result.returncode == 0, f"{script_path} status returned non-zero exit code {result.returncode}. Ensure all apps are running and PID files exist."

def test_haproxy_running():
    result = subprocess.run(['pgrep', 'haproxy'], capture_output=True)
    assert result.returncode == 0, "haproxy process is not running."

def test_proxy_results_log():
    log_path = '/home/user/proxy_results.log'
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(lines) == 12, f"Expected exactly 12 lines in {log_path}, found {len(lines)}."
    for i, line in enumerate(lines):
        assert line == "200", f"Line {i+1} in {log_path} is '{line}', expected '200'."

def test_verify_restore_script_exists():
    script_path = '/home/user/verify_restore.sh'
    assert os.path.isfile(script_path), f"Verification script {script_path} does not exist."