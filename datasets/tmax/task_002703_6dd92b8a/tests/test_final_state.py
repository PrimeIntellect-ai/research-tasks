# test_final_state.py

import os
import subprocess
import tempfile
import shutil
import re
import pytest

def run_cmd(cmd, cwd=None):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)

def test_bare_repository_exists():
    repo_path = "/home/user/auth_server.git"
    assert os.path.isdir(repo_path), f"Bare repository directory {repo_path} does not exist."
    result = run_cmd("git rev-parse --is-bare-repository", cwd=repo_path)
    assert result.returncode == 0, f"Git command failed in {repo_path}."
    assert result.stdout.strip() == "true", f"Repository at {repo_path} is not a bare repository."

def test_pre_receive_hook_exists_and_executable():
    hook_path = "/home/user/auth_server.git/hooks/pre-receive"
    assert os.path.isfile(hook_path), f"Pre-receive hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Pre-receive hook {hook_path} is not executable."

def test_extract_emails_script_exists_and_executable():
    script_path = "/home/user/extract_emails.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_cron_configuration():
    cron_path = "/home/user/my_cron.txt"
    assert os.path.isfile(cron_path), f"Cron configuration {cron_path} does not exist."
    with open(cron_path, "r") as f:
        content = f.read().strip()

    # Matches: 0 2 * * * /home/user/extract_emails.sh
    # Allowing for varying amounts of whitespace
    pattern = r"^0\s+2\s+\*\s+\*\s+\*\s+/home/user/extract_emails\.sh$"
    assert re.match(pattern, content), f"Cron configuration in {cron_path} does not match expected format."

def test_git_workflow_and_hook_enforcement():
    repo_path = "/home/user/auth_server.git"

    with tempfile.TemporaryDirectory() as temp_dir:
        clone_cmd = f"git clone {repo_path} {temp_dir}"
        assert run_cmd(clone_cmd).returncode == 0, "Failed to clone the bare repository."

        # Configure git user
        run_cmd("git config user.name 'Test User'", cwd=temp_dir)
        run_cmd("git config user.email 'test@example.com'", cwd=temp_dir)

        accounts_dir = os.path.join(temp_dir, "accounts")
        os.makedirs(accounts_dir, exist_ok=True)

        # Test 1: Banned user
        banned_file = os.path.join(accounts_dir, "admin.json")
        with open(banned_file, "w") as f:
            f.write('{"email": "admin@test.com"}')
        run_cmd("git add accounts/admin.json", cwd=temp_dir)
        run_cmd("git commit -m 'Add admin'", cwd=temp_dir)
        push_result = run_cmd("git push origin master", cwd=temp_dir)
        if push_result.returncode == 0:
            # Maybe the default branch is main
            push_result = run_cmd("git push origin main", cwd=temp_dir)
        assert push_result.returncode != 0, "Pushing a banned user account should have been rejected."

        # Reset
        run_cmd("git reset --hard HEAD~1", cwd=temp_dir)
        os.remove(banned_file)

        # Test 2: Invalid JSON
        invalid_json_file = os.path.join(accounts_dir, "validuser.json")
        with open(invalid_json_file, "w") as f:
            f.write('{"email": "valid@test.com"') # Missing closing brace
        run_cmd("git add accounts/validuser.json", cwd=temp_dir)
        run_cmd("git commit -m 'Add invalid json'", cwd=temp_dir)
        push_result = run_cmd("git push origin HEAD", cwd=temp_dir)
        assert push_result.returncode != 0, "Pushing invalid JSON should have been rejected."

        # Reset
        run_cmd("git reset --hard HEAD~1", cwd=temp_dir)
        os.remove(invalid_json_file)

        # Test 3: Missing email
        missing_email_file = os.path.join(accounts_dir, "noemail.json")
        with open(missing_email_file, "w") as f:
            f.write('{"name": "No Email"}')
        run_cmd("git add accounts/noemail.json", cwd=temp_dir)
        run_cmd("git commit -m 'Add missing email'", cwd=temp_dir)
        push_result = run_cmd("git push origin HEAD", cwd=temp_dir)
        assert push_result.returncode != 0, "Pushing JSON without email key should have been rejected."

        # Reset
        run_cmd("git reset --hard HEAD~1", cwd=temp_dir)
        os.remove(missing_email_file)

        # Test 4: Valid users
        alice_file = os.path.join(accounts_dir, "alice.json")
        with open(alice_file, "w") as f:
            f.write('{\n  "email": "alice@domain.com"\n}')
        bob_file = os.path.join(accounts_dir, "bob.json")
        with open(bob_file, "w") as f:
            f.write('{\n  "email": "bob@domain.com"\n}')

        run_cmd("git add accounts/alice.json accounts/bob.json", cwd=temp_dir)
        run_cmd("git commit -m 'Add valid users'", cwd=temp_dir)
        push_result = run_cmd("git push origin HEAD", cwd=temp_dir)
        assert push_result.returncode == 0, f"Pushing valid users failed: {push_result.stderr}"

def test_extract_emails_execution():
    script_path = "/home/user/extract_emails.sh"
    output_csv = "/home/user/active_emails.csv"

    # Remove existing csv if any
    if os.path.exists(output_csv):
        os.remove(output_csv)

    result = run_cmd(script_path)
    assert result.returncode == 0, f"Executing {script_path} failed: {result.stderr}"
    assert os.path.isfile(output_csv), f"Output file {output_csv} was not created."

    with open(output_csv, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_entries = {"alice,alice@domain.com", "bob,bob@domain.com"}
    actual_entries = set(lines)

    assert expected_entries.issubset(actual_entries), f"Missing expected entries in CSV. Expected: {expected_entries}, Found: {actual_entries}"