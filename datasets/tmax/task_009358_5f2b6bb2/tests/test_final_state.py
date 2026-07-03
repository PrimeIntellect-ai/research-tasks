# test_final_state.py

import os
import subprocess
import tempfile
import stat

def test_quota_check_executable():
    """Verify the quota_check C++ executable exists and behaves correctly."""
    exe_path = "/home/user/quota_check"
    assert os.path.isfile(exe_path), f"{exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

    # Create a temporary directory to test the quota check
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a 2MB file
        with open(os.path.join(tmpdir, "test1.dat"), "wb") as f:
            f.write(b"0" * (2 * 1024 * 1024))

        # Test under quota
        result_ok = subprocess.run(
            [exe_path, tmpdir, "3000000"],
            capture_output=True, text=True
        )
        assert result_ok.returncode == 0, f"quota_check failed to return 0 for under-quota directory. Output: {result_ok.stdout}"
        assert result_ok.stdout.strip() == "OK", "quota_check did not print 'OK' for under-quota directory."

        # Test over quota
        result_exceeded = subprocess.run(
            [exe_path, tmpdir, "1000000"],
            capture_output=True, text=True
        )
        assert result_exceeded.returncode == 1, "quota_check failed to return 1 for over-quota directory."
        assert result_exceeded.stdout.strip() == "QUOTA EXCEEDED", "quota_check did not print 'QUOTA EXCEEDED' for over-quota directory."

def test_git_restore_target():
    """Verify the restore_target.git bare repository exists."""
    repo_path = "/home/user/restore_target.git"
    assert os.path.isdir(repo_path), f"{repo_path} does not exist."
    assert os.path.isfile(os.path.join(repo_path, "config")), f"{repo_path} does not look like a git repository."

    # Check if it's a bare repo
    result = subprocess.run(
        ["git", "rev-parse", "--is-bare-repository"],
        cwd=repo_path, capture_output=True, text=True
    )
    assert result.stdout.strip() == "true", f"{repo_path} is not a bare repository."

def test_pre_receive_hook():
    """Verify the pre-receive hook exists and is executable."""
    hook_path = "/home/user/restore_target.git/hooks/pre-receive"
    assert os.path.isfile(hook_path), f"{hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"{hook_path} is not executable."

def test_socat_port_forwarding():
    """Verify socat is running with the correct PID and arguments."""
    pid_file = "/home/user/socat.pid"
    assert os.path.isfile(pid_file), f"{pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer."
    pid = int(pid_str)

    # Check if process is running
    assert os.path.isdir(f"/proc/{pid}"), f"Process with PID {pid} is not running."

    # Check process command line
    with open(f"/proc/{pid}/cmdline", "r") as f:
        cmdline = f.read().replace('\x00', ' ').strip()

    assert "socat" in cmdline, f"Process {pid} is not socat. Cmdline: {cmdline}"
    assert "18080" in cmdline, f"socat is not listening on port 18080. Cmdline: {cmdline}"
    assert "19090" in cmdline, f"socat is not forwarding to 19090. Cmdline: {cmdline}"

def test_push_failed_log():
    """Verify the push_failed.log contains the expected output."""
    log_path = "/home/user/push_failed.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "QUOTA EXCEEDED" in log_content, f"'QUOTA EXCEEDED' not found in {log_path}."

def test_backup_client_repo():
    """Verify the backup_client repository and payload file."""
    client_path = "/home/user/backup_client"
    assert os.path.isdir(client_path), f"{client_path} does not exist."
    assert os.path.isdir(os.path.join(client_path, ".git")), f"{client_path} is not a git repository."

    payload_path = os.path.join(client_path, "payload.dat")
    assert os.path.isfile(payload_path), f"{payload_path} does not exist."

    # Check size is around 6MB (allow some variance, e.g., > 5MB)
    size = os.path.getsize(payload_path)
    assert size > 5000000, f"{payload_path} is too small to trigger the quota."