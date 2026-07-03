# test_final_state.py

import os
import stat
import tarfile
import re
import pytest

def test_directories_exist():
    """Check that the required directories have been created."""
    dirs = [
        "/home/user/user_registry.git",
        "/home/user/active_users",
        "/home/user/backups"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist."

def test_bare_repo_exists():
    """Check that the bare repository is initialized."""
    config_path = "/home/user/user_registry.git/config"
    assert os.path.isfile(config_path), f"Git bare repo config not found at {config_path}."

def test_hook_executable_elf():
    """Check that the post-receive hook is an executable ELF binary."""
    hook_path = "/home/user/user_registry.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Post-receive hook not found at {hook_path}."

    # Check if executable
    st = os.stat(hook_path)
    assert st.st_mode & stat.S_IXUSR, f"Post-receive hook {hook_path} is not executable."

    # Check if ELF
    with open(hook_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"Post-receive hook {hook_path} is not a compiled ELF binary."

def test_deployed_file():
    """Check that the master branch was checked out to active_users."""
    conf_path = "/home/user/active_users/admin_user.conf"
    assert os.path.isfile(conf_path), f"Deployed file not found at {conf_path}."

    with open(conf_path, "r") as f:
        content = f.read()
    assert "role=superuser" in content, f"Expected 'role=superuser' in {conf_path}."

def test_backup_archive():
    """Check the backup tarball exists, has correct permissions, and contains the file."""
    tar_path = "/home/user/backups/latest.tar.gz"
    assert os.path.isfile(tar_path), f"Backup archive not found at {tar_path}."

    # Check permissions (exactly 0400)
    st = os.stat(tar_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Permissions for {tar_path} must be exactly 0400, got {oct(perms)}."

    # Verify archive contents
    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar archive."
    with tarfile.open(tar_path, "r:gz") as tar:
        names = tar.getnames()
        # The file might be stored as active_users/admin_user.conf or just admin_user.conf
        found = any("admin_user.conf" in name for name in names)
        assert found, f"admin_user.conf not found inside the backup archive {tar_path}."

def test_sync_log():
    """Check that the sync log contains the correctly formatted timestamp and message."""
    log_path = "/home/user/sync.log"
    assert os.path.isfile(log_path), f"Log file not found at {log_path}."

    with open(log_path, "r") as f:
        content = f.read()

    # Regex to match: [YYYY-MM-DD HH:MM:SS JST] Registry updated
    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} JST\] Registry updated$"

    match_found = False
    for line in content.splitlines():
        if re.match(pattern, line.strip()):
            match_found = True
            break

    assert match_found, f"Log file {log_path} does not contain the correctly formatted JST log entry."