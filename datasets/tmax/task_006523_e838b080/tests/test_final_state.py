# test_final_state.py

import os
import stat
import subprocess
import tempfile
import shutil
import pytest

def test_env_profile_contents():
    path = "/home/user/.env_profile"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "APP_PORT=8080" in content or "APP_PORT=\"8080\"" in content or "APP_PORT='8080'" in content, "APP_PORT is not correctly set to 8080."
    assert "APP_ENV=production" in content or "APP_ENV=\"production\"" in content or "APP_ENV='production'" in content, "APP_ENV is not correctly set to production."
    assert "export APP_PORT" in content or "export APP_ENV" in content or "export APP_PORT=8080" in content or "export APP_ENV=production" in content, "Variables must be exported."

def test_monitor_storage_executable():
    path = "/home/user/monitor_storage"
    assert os.path.isfile(path), f"File {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_run_app_executable():
    path = "/home/user/run_app.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."
    with open(path, "r") as f:
        content = f.read()
    assert "set -e" in content or "set -o errexit" in content, "run_app.sh must enable strict error handling (e.g., set -e)."

def test_monitor_storage_missing_dir():
    path = "/home/user/monitor_storage"
    result = subprocess.run([path, "/non_existent_dir_12345"], capture_output=True, text=True)
    assert result.returncode == 1, "monitor_storage should exit with status 1 for a missing directory."
    assert "Error: Directory not found" in result.stderr.strip(), "monitor_storage did not print the correct error message to stderr."

def test_monitor_storage_small_dir():
    path = "/home/user/monitor_storage"
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a small file
        with open(os.path.join(temp_dir, "small.txt"), "wb") as f:
            f.write(b"0" * 100)

        result = subprocess.run([path, temp_dir], capture_output=True, text=True)
        assert result.returncode == 0, "monitor_storage should exit with status 0 for a small directory."
        assert result.stdout.strip() == "STATUS: OK", "monitor_storage should print exactly 'STATUS: OK' for a small directory."

def test_monitor_storage_large_dir():
    path = "/home/user/monitor_storage"
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a large file > 1MB
        with open(os.path.join(temp_dir, "large.txt"), "wb") as f:
            f.write(b"0" * 1000001)
        # Create a .old file
        old_file = os.path.join(temp_dir, "test.old")
        with open(old_file, "wb") as f:
            f.write(b"old data")

        result = subprocess.run([path, temp_dir], capture_output=True, text=True)
        assert result.returncode == 0, "monitor_storage should exit with status 0 for a large directory."
        assert result.stdout.strip() == "STATUS: CLEANED", "monitor_storage should print exactly 'STATUS: CLEANED' for a large directory."
        assert not os.path.exists(old_file), "monitor_storage failed to delete the .old file."

def test_run_app_execution_and_status():
    # Execute run_app.sh to ensure it works and appends correctly
    # We will recreate a large log to ensure it cleans it up, just in case the student didn't run it
    log_dir = "/home/user/app_logs"
    os.makedirs(log_dir, exist_ok=True)
    large_log = os.path.join(log_dir, "large_log.old")
    with open(large_log, "wb") as f:
        f.write(b"0" * 1200000)

    run_app_path = "/home/user/run_app.sh"
    result = subprocess.run([run_app_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_app.sh failed to execute properly. stderr: {result.stderr}"

    assert not os.path.exists(large_log), "run_app.sh did not result in the .old file being deleted."

    status_log = "/home/user/app_status.log"
    assert os.path.isfile(status_log), f"File {status_log} was not created."
    with open(status_log, "r") as f:
        content = f.read()

    expected_line = "[SUCCESS] Environment production initialized on port 8080"
    assert expected_line in content, f"Expected line '{expected_line}' not found in {status_log}."