# test_final_state.py

import os
import stat
import pytest

def test_directories_exist():
    """Verify that all required directories were created."""
    directories = [
        "/home/user/logs",
        "/home/user/config",
        "/home/user/bin",
        "/home/user/run",
        "/home/user/old_data",
        "/home/user/deploy_worktree",
    ]
    for d in directories:
        assert os.path.isdir(d), f"Required directory {d} is missing or not a directory."

def test_initial_files_content():
    """Verify the content of hello.txt and virtual_fstab."""
    hello_path = "/home/user/old_data/hello.txt"
    assert os.path.isfile(hello_path), f"{hello_path} does not exist."
    with open(hello_path, "r") as f:
        assert f.read().strip() == "MIGRATION_READY", f"Content of {hello_path} is incorrect."

    fstab_path = "/home/user/config/virtual_fstab"
    assert os.path.isfile(fstab_path), f"{fstab_path} does not exist."
    with open(fstab_path, "r") as f:
        assert f.read().strip() == "/home/user/old_data /home/user/new_data/mnt", f"Content of {fstab_path} is incorrect."

def test_git_repo_and_hook():
    """Verify the bare git repository and post-receive hook."""
    hook_path = "/home/user/migration_repo.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} does not exist."
    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Git hook {hook_path} is not executable."

def test_service_management_script():
    """Verify the restart_service.sh script exists and is executable."""
    script_path = "/home/user/bin/restart_service.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_log_file_content():
    """Verify the migration log contains the expected output."""
    log_path = "/home/user/logs/migration.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    expected_log = "MOUNTED /home/user/old_data TO /home/user/new_data/mnt"
    with open(log_path, "r") as f:
        content = f.read()
        assert expected_log in content, f"Log file {log_path} does not contain the expected string."

def test_symlink_and_mount_content():
    """Verify the symlink was created correctly and points to the right data."""
    mnt_path = "/home/user/new_data/mnt"
    assert os.path.islink(mnt_path), f"{mnt_path} is not a symlink."

    target = os.readlink(mnt_path)
    assert target == "/home/user/old_data", f"Symlink points to {target} instead of /home/user/old_data."

    hello_mnt_path = os.path.join(mnt_path, "hello.txt")
    assert os.path.isfile(hello_mnt_path), f"{hello_mnt_path} cannot be accessed through the symlink."
    with open(hello_mnt_path, "r") as f:
        assert f.read().strip() == "MIGRATION_READY", "Content read through symlink is incorrect."

def test_daemon_is_running():
    """Verify the PID file exists and the daemon process is running."""
    pid_file = "/home/user/run/migrator.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid PID."
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} from {pid_file} is not running.")