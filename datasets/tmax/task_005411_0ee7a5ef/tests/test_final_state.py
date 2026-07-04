# test_final_state.py

import os
import subprocess
import pytest

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.stdout.strip(), result.returncode

def test_hook_is_executable_binary():
    hook_path = "/home/user/app.git/hooks/post-receive"
    assert os.path.exists(hook_path), f"Hook file {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Hook file {hook_path} is not executable."

    # Check if it's an ELF binary
    with open(hook_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"Hook file {hook_path} is not an ELF binary. Did you compile it with Rust?"

def test_git_commits_and_symlink():
    repo_dir = "/home/user/app.git"
    assert os.path.isdir(repo_dir), f"Bare repository {repo_dir} does not exist."

    out, code = run_cmd("git rev-list --max-parents=0 HEAD", cwd=repo_dir)
    assert code == 0, "Failed to get the first commit hash."
    commit1 = out

    out, code = run_cmd("git rev-parse HEAD", cwd=repo_dir)
    assert code == 0, "Failed to get the latest commit hash."
    commit2 = out

    symlink_path = "/home/user/deploy/current"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    target = os.readlink(symlink_path)
    expected_target = f"/home/user/deploy/releases/{commit2}"

    # Resolve absolute paths to be safe
    abs_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
    assert abs_target == expected_target, f"Symlink points to {abs_target}, expected {expected_target}."

def test_planner_log():
    repo_dir = "/home/user/app.git"
    log_path = "/home/user/deploy/planner_log.txt"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    out, code = run_cmd("git rev-list --max-parents=0 HEAD", cwd=repo_dir)
    commit1 = out

    out, code = run_cmd("git rev-parse HEAD", cwd=repo_dir)
    commit2 = out

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {log_path}, found {len(lines)}."

    expected_line1 = f"DEPLOYMENT {commit1} REQUIRES CPU: 4 cores, RAM: 16GB"
    expected_line2 = f"DEPLOYMENT {commit2} REQUIRES CPU: 8 cores, RAM: 32GB"

    assert lines[0] == expected_line1, f"First line of log is incorrect. Expected: '{expected_line1}', Got: '{lines[0]}'"
    assert lines[1] == expected_line2, f"Second line of log is incorrect. Expected: '{expected_line2}', Got: '{lines[1]}'"