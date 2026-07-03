# test_final_state.py

import os
import stat
import subprocess
import tempfile
import tarfile
import re

def test_directories_and_permissions():
    """Verify scripts and backups directories exist, and backups has 700 permissions."""
    scripts_dir = "/home/user/scripts"
    backups_dir = "/home/user/backups"

    assert os.path.isdir(scripts_dir), f"Directory {scripts_dir} does not exist."
    assert os.path.isdir(backups_dir), f"Directory {backups_dir} does not exist."

    st = os.stat(backups_dir)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Permissions for {backups_dir} are {oct(perms)}, expected 0o700."

def test_git_repo_is_bare():
    """Verify the git repository is bare."""
    git_dir = "/home/user/edge_config.git"
    assert os.path.isdir(git_dir), f"Git repo directory {git_dir} does not exist."

    config_file = os.path.join(git_dir, "config")
    assert os.path.isfile(config_file), f"Git config file {config_file} does not exist."

    try:
        output = subprocess.check_output(
            ["git", "-C", git_dir, "config", "--get", "core.bare"],
            stderr=subprocess.STDOUT,
            text=True
        ).strip()
    except subprocess.CalledProcessError:
        output = ""

    assert output == "true", f"Git repository at {git_dir} is not bare (core.bare={output})."

def test_post_receive_hook_exists_and_executable():
    """Verify the post-receive hook exists, is executable, and is a Python script."""
    hook_path = "/home/user/edge_config.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook file {hook_path} does not exist."

    assert os.access(hook_path, os.X_OK), f"Hook file {hook_path} is not executable."

    with open(hook_path, 'r') as f:
        first_line = f.readline().strip()

    assert "python" in first_line.lower(), f"Hook {hook_path} does not appear to be a Python script (shebang: {first_line})."

def test_crontab_schedule():
    """Verify the crontab contains the correct schedule for sync_data.sh."""
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        output = ""

    pattern = re.compile(r"^\s*(?:\*/15|0,15,30,45)\s+\*\s+\*\s+\*\s+\*\s+/home/user/scripts/sync_data\.sh", re.MULTILINE)
    assert pattern.search(output), f"Crontab does not contain the expected schedule for sync_data.sh. Current crontab:\n{output}"

def test_git_push_triggers_backup():
    """Simulate a git push to trigger the hook, verify output and backup archive."""
    git_dir = "/home/user/edge_config.git"
    backup_archive = "/home/user/backups/state_backup.tar.gz"

    # Remove backup archive if it exists from previous tests or manual runs
    if os.path.exists(backup_archive):
        os.remove(backup_archive)

    with tempfile.TemporaryDirectory() as temp_dir:
        clone_dir = os.path.join(temp_dir, "edge_config")

        # Clone
        subprocess.check_call(["git", "clone", git_dir, clone_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Commit
        test_file = os.path.join(clone_dir, "test.conf")
        with open(test_file, "w") as f:
            f.write("new_config=1\n")

        subprocess.check_call(["git", "-C", clone_dir, "add", "test.conf"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Set git user info for commit
        subprocess.check_call(["git", "-C", clone_dir, "config", "user.email", "test@example.com"])
        subprocess.check_call(["git", "-C", clone_dir, "config", "user.name", "Test User"])

        subprocess.check_call(["git", "-C", clone_dir, "commit", "-m", "Test commit"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Push and capture output
        push_process = subprocess.run(
            ["git", "-C", clone_dir, "push", "origin", "master"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        output = push_process.stdout

        assert "Deployment received, backing up..." in output, \
            f"Expected output not found in git push. Output was:\n{output}"

        assert os.path.isfile(backup_archive), f"Backup archive {backup_archive} was not created after git push."

        # Verify tarball contents
        with tarfile.open(backup_archive, "r:gz") as tar:
            names = tar.getnames()

        assert any("sensor.conf" in name for name in names), \
            f"Backup archive does not contain sensor.conf. Contents: {names}"