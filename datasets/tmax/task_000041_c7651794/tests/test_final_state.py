# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_service_status_file():
    status_file = "/home/user/service_status.txt"
    assert os.path.isfile(status_file), f"File {status_file} does not exist."
    with open(status_file, "r") as f:
        content = f.read().strip()
    assert content == "active", f"Expected 'active' in {status_file}, but got '{content}'."

def test_repair_script_exists_and_executable():
    script_path = "/home/user/repair.sh"
    assert os.path.isfile(script_path), f"Repair script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Repair script {script_path} is not executable."

def test_symlink_fixed():
    symlink_path = "/home/user/.config/micro-proxy/sites-enabled/default.conf"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    assert os.path.exists(symlink_path), f"Symlink {symlink_path} is broken."

    target = os.readlink(symlink_path)
    expected_target = "/home/user/.config/micro-proxy/sites-available/default.conf"
    # It could be an absolute path or relative path, let's resolve it.
    assert os.path.realpath(symlink_path) == os.path.realpath(expected_target), \
        f"Symlink does not resolve to {expected_target}."

def test_log_quota_fixed():
    log_dir = "/home/user/proxy-logs"
    assert os.path.isdir(log_dir), f"Directory {log_dir} does not exist."

    # Check total size of the directory in MB
    total_size = 0
    for dirpath, _, filenames in os.walk(log_dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    size_mb = total_size / (1024 * 1024)
    assert size_mb <= 50, f"Log directory size is {size_mb} MB, which still exceeds the 50 MB quota."

def test_service_is_active():
    # Set XDG_RUNTIME_DIR to ensure systemctl --user works
    uid = os.getuid()
    env = os.environ.copy()
    env["XDG_RUNTIME_DIR"] = f"/run/user/{uid}"

    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "micro-proxy.service"],
            env=env,
            capture_output=True,
            text=True,
            check=False
        )
        assert result.returncode == 0, f"Service micro-proxy.service is not active. Output: {result.stdout.strip()}"
        assert result.stdout.strip() == "active", f"Service is not active, status is '{result.stdout.strip()}'."
    except FileNotFoundError:
        pytest.fail("systemctl command not found.")