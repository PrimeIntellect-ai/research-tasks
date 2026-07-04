# test_final_state.py

import os
import stat
import subprocess

def test_hook_alerts_log():
    log_path = "/home/user/hook_alerts.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 1, f"Log file {log_path} is empty."
    assert "ALERT: File critical.txt was modified" in lines, f"Log file {log_path} does not contain the expected alert message."

def test_setup_hook_py_exists_and_idempotent():
    script_path = "/home/user/setup_hook.py"
    assert os.path.isfile(script_path), f"Setup script {script_path} is missing."

    hook_path = "/home/user/alerts_repo.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook file {hook_path} is missing."

    # Read original hook content
    with open(hook_path, "r") as f:
        original_hook_content = f.read()

    # Run the setup script again to check idempotency
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {script_path} failed on repeated execution."

    # Check if hook content remains valid/uncorrupted
    with open(hook_path, "r") as f:
        new_hook_content = f.read()

    # It shouldn't just infinitely append the same script
    assert len(new_hook_content) < len(original_hook_content) * 2, "Setup script does not appear to be idempotent (it might be appending to the hook file indefinitely)."

def test_post_receive_hook_executable():
    hook_path = "/home/user/alerts_repo.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook file {hook_path} is missing."

    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Hook file {hook_path} is not executable."

def test_trigger_exp_exists():
    exp_path = "/home/user/trigger.exp"
    assert os.path.isfile(exp_path), f"Expect script {exp_path} is missing."

def test_workspace_state():
    workspace_file = "/home/user/workspace/critical.txt"
    assert os.path.isfile(workspace_file), f"File {workspace_file} was not created in the workspace."

    with open(workspace_file, "r") as f:
        content = f.read().strip()

    assert content == "HIGH: Database connection lost", f"Content of {workspace_file} is incorrect."

    # Check if it was pushed to the bare repo
    bare_repo = "/home/user/alerts_repo.git"
    result = subprocess.run(["git", "-C", bare_repo, "ls-tree", "-r", "master", "--name-only"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to inspect bare repository."
    assert "critical.txt" in result.stdout.splitlines(), "critical.txt was not pushed to the bare repository."