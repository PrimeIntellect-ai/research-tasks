# test_final_state.py
import os
import stat
import subprocess
import shutil

def test_git_repo_and_symlink():
    repo_dir = "/home/user/net-conf.git"
    symlink_path = "/home/user/active-repo"

    # Check bare repo
    assert os.path.isdir(repo_dir), f"Directory {repo_dir} does not exist."
    assert os.path.isfile(os.path.join(repo_dir, "HEAD")), f"{repo_dir} does not appear to be a bare git repository (missing HEAD)."
    assert os.path.isdir(os.path.join(repo_dir, "objects")), f"{repo_dir} does not appear to be a bare git repository (missing objects dir)."
    assert os.path.isdir(os.path.join(repo_dir, "refs")), f"{repo_dir} does not appear to be a bare git repository (missing refs dir)."

    # Check symlink
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    target = os.readlink(symlink_path)
    assert target == repo_dir, f"Symlink {symlink_path} points to {target}, expected {repo_dir}."

def test_repo_quota_config():
    config_file = "/home/user/.config/repo_quota"
    assert os.path.isfile(config_file), f"Config file {config_file} does not exist."
    with open(config_file, "r") as f:
        content = f.read().strip()
    assert content == "2048", f"Config file {config_file} contains '{content}', expected '2048'."

def test_bash_profile():
    profile_file = "/home/user/.bash_profile"
    assert os.path.isfile(profile_file), f"Profile file {profile_file} does not exist."
    with open(profile_file, "r") as f:
        content = f.read()

    assert 'GIT_AUTHOR_NAME="SysAdmin"' in content, f"GIT_AUTHOR_NAME not found in {profile_file}."
    assert 'GIT_AUTHOR_EMAIL="sysadmin@local"' in content, f"GIT_AUTHOR_EMAIL not found in {profile_file}."
    assert 'NETWORK_ENV="hardening"' in content, f"NETWORK_ENV not found in {profile_file}."

def test_git_hook_logic():
    repo_dir = "/home/user/net-conf.git"
    hook_path = os.path.join(repo_dir, "hooks", "pre-receive")
    config_file = "/home/user/.config/repo_quota"

    assert os.path.isfile(hook_path), f"Hook file {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Hook file {hook_path} is not executable."

    # Backup config
    with open(config_file, "r") as f:
        original_quota = f.read()

    try:
        # Test quota exceeded
        with open(config_file, "w") as f:
            f.write("1\n")

        result = subprocess.run(
            [hook_path], 
            cwd=repo_dir, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        assert result.returncode != 0, "Hook should have failed (non-zero exit code) when quota is exceeded."
        assert "QUOTA EXCEEDED" in result.stderr, "Hook did not print 'QUOTA EXCEEDED' to stderr when quota is exceeded."

        # Test quota not exceeded
        with open(config_file, "w") as f:
            f.write("9999999\n")

        result2 = subprocess.run(
            [hook_path], 
            cwd=repo_dir, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        assert result2.returncode == 0, "Hook should have succeeded (exit code 0) when quota is not exceeded."

    finally:
        # Restore config
        with open(config_file, "w") as f:
            f.write(original_quota)

def test_completion_log():
    log_file = "/home/user/completion.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 3, f"Log file {log_file} does not have at least 3 lines."
    assert lines[0] == "/home/user/net-conf.git", f"Line 1 of {log_file} is incorrect."
    assert lines[1] == "/home/user/net-conf.git/hooks/pre-receive", f"Line 2 of {log_file} is incorrect."

    # The 3rd line should be an octal permission like 755
    perms = lines[2].strip()
    assert perms.isdigit() and len(perms) in (3, 4), f"Line 3 of {log_file} does not look like an octal permission: '{perms}'."

    # Check if the actual file matches the stated permissions
    hook_path = lines[1]
    if os.path.exists(hook_path):
        actual_mode = stat.S_IMODE(os.stat(hook_path).st_mode)
        actual_octal = oct(actual_mode).replace('0o', '')
        # Allow matching either e.g. '755' or '0755'
        assert actual_octal.endswith(perms[-3:]), f"Stated permissions '{perms}' do not match actual permissions '{actual_octal}'."