# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_check_ban_c_exists():
    assert os.path.isfile("/home/user/check_ban.c"), "/home/user/check_ban.c does not exist."

def test_check_ban_executable_behavior():
    executable = "/home/user/check_ban"
    assert os.path.isfile(executable), f"{executable} does not exist."
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f_banned:
        f_banned.write("Username: bad\nRole: guest\nStatus: BANNED\n")
        banned_path = f_banned.name

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f_active:
        f_active.write("Username: good\nRole: dev\nStatus: ACTIVE\n")
        active_path = f_active.name

    try:
        # Test banned
        result_banned = subprocess.run([executable, banned_path], capture_output=True, text=True)
        assert result_banned.returncode == 1, "check_ban did not exit with status 1 for a BANNED profile."
        assert "Banned user detected" in result_banned.stdout, "check_ban did not print the expected message for a BANNED profile."

        # Test active
        result_active = subprocess.run([executable, active_path], capture_output=True, text=True)
        assert result_active.returncode == 0, "check_ban did not exit with status 0 for an ACTIVE profile."
    finally:
        os.remove(banned_path)
        os.remove(active_path)

def test_build_profiles_exp_exists():
    assert os.path.isfile("/home/user/build_profiles.exp"), "/home/user/build_profiles.exp does not exist."

def test_git_repo_and_hook():
    git_dir = "/home/user/profiles/.git"
    assert os.path.isdir(git_dir), "Git repository was not initialized in /home/user/profiles/."

    hook_path = os.path.join(git_dir, "hooks", "pre-commit")
    assert os.path.isfile(hook_path), f"pre-commit hook does not exist at {hook_path}."
    assert os.access(hook_path, os.X_OK), f"pre-commit hook at {hook_path} is not executable."

def test_git_commit_status():
    repo_dir = "/home/user/profiles"

    # Check that files were generated
    for user in ["admin1", "user1", "baduser"]:
        assert os.path.isfile(os.path.join(repo_dir, f"{user}.txt")), f"{user}.txt was not generated in {repo_dir}."

    # Check committed files
    result_ls = subprocess.run(["git", "ls-tree", "-r", "HEAD", "--name-only"], cwd=repo_dir, capture_output=True, text=True)
    assert result_ls.returncode == 0, "Failed to get git ls-tree. Is there a commit?"
    committed_files = result_ls.stdout.strip().split('\n')

    assert "admin1.txt" in committed_files, "admin1.txt is not committed."
    assert "user1.txt" in committed_files, "user1.txt is not committed."
    assert "baduser.txt" not in committed_files, "baduser.txt should not be committed."

def test_success_log():
    log_path = "/home/user/success_log.txt"
    assert os.path.isfile(log_path), f"{log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "Initial profiles", f"success_log.txt contains '{content}' instead of 'Initial profiles'."