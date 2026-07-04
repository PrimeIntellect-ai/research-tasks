# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_hook_executable_exists():
    hook_path = "/home/user/alerts.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook executable not found at {hook_path}"

    # Check if executable
    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Hook at {hook_path} is not executable"

def test_hook_functionality(tmp_path):
    hook_path = "/home/user/alerts.git/hooks/post-receive"
    log_path = "/home/user/push.log"

    # Backup existing log if any
    if os.path.exists(log_path):
        os.rename(log_path, log_path + ".bak")

    try:
        # Run the hook with mock input
        input_data = "0000000000000000000000000000000000000000 1111111111111111111111111111111111111111 refs/heads/test_branch\n"
        process = subprocess.run([hook_path], input=input_data, text=True, capture_output=True)
        assert process.returncode == 0, "Hook execution failed"

        assert os.path.isfile(log_path), f"Log file {log_path} was not created by the hook"

        with open(log_path, "r") as f:
            content = f.read()

        assert "[MONITOR] refs/heads/test_branch updated" in content, "Log file does not contain the expected formatted string"
    finally:
        # Restore log
        if os.path.exists(log_path):
            os.remove(log_path)
        if os.path.exists(log_path + ".bak"):
            os.rename(log_path + ".bak", log_path)

def test_expect_script():
    script_path = "/home/user/push_test.exp"
    assert os.path.isfile(script_path), f"Expect script not found at {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    assert "spawn" in content, "Expect script does not use 'spawn'"
    assert "git push" in content, "Expect script does not contain 'git push'"
    assert "/home/user/alerts.git" in content, "Expect script does not push to the correct bare repository"
    assert "HEAD:main" in content, "Expect script does not push HEAD:main"
    assert "eof" in content.lower(), "Expect script does not wait for EOF"

def test_cron_job():
    try:
        result = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True, check=True)
        cron_output = result.stdout
    except subprocess.CalledProcessError:
        try:
            # Fallback to current user if running as user
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
            cron_output = result.stdout
        except subprocess.CalledProcessError:
            pytest.fail("Failed to retrieve crontab. Is it set up?")

    assert "/usr/bin/expect" in cron_output, "Cron job does not call /usr/bin/expect"
    assert "/home/user/push_test.exp" in cron_output, "Cron job does not execute the expect script"

    # Check if it runs every minute
    lines = cron_output.strip().split('\n')
    found_cron = False
    for line in lines:
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 5:
            schedule = " ".join(parts[:5])
            if schedule == "* * * * *" and "/home/user/push_test.exp" in line:
                found_cron = True
                break

    assert found_cron, "Could not find a cron job scheduled to run every minute (* * * * *) for the expect script"