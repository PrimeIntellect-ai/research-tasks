# test_final_state.py

import os
import json
import subprocess
import pytest

def test_monitor_script_executable():
    script_path = "/home/user/monitor_script"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_crontab_entry():
    try:
        output = subprocess.check_output(['crontab', '-l'], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Has it been set up?")

    valid_cron_found = False
    for line in output.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '/home/user/monitor_script' in line:
            parts = line.split()
            if len(parts) >= 6:
                minute_field = parts[0]
                # Check for common valid 10-minute intervals
                if minute_field in ('*/10', '0,10,20,30,40,50'):
                    valid_cron_found = True
                    break

    assert valid_cron_found, "Could not find a valid crontab entry running /home/user/monitor_script every 10 minutes."

def test_alert_log_contents():
    log_path = "/home/user/alert.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did the script run?"

    with open(log_path, "r") as f:
        log_content = f.read().splitlines()

    users_list_path = "/home/user/users_list.txt"
    quotas_path = "/home/user/quotas.json"

    assert os.path.isfile(users_list_path), f"{users_list_path} is missing."
    assert os.path.isfile(quotas_path), f"{quotas_path} is missing."

    with open(users_list_path, "r") as f:
        users = [line.strip() for line in f if line.strip()]

    with open(quotas_path, "r") as f:
        quotas = json.load(f)

    for user in users:
        # Get du -sb output
        du_cmd = ["du", "-sb", f"/home/user/data/users/{user}"]
        try:
            du_output = subprocess.check_output(du_cmd, text=True)
            usage_bytes = int(du_output.split()[0])
        except Exception as e:
            pytest.fail(f"Failed to calculate usage for {user}: {e}")

        quota = quotas.get(user)
        assert quota is not None, f"Quota for {user} not found."

        expected_log_line = f"ALERT: User {user} exceeded quota. Usage: {usage_bytes}, Quota: {quota}"

        # Check if log contains this user
        user_in_log = any(f"User {user} " in line for line in log_content)

        if usage_bytes > quota:
            assert expected_log_line in log_content, f"Expected alert for {user} not found or incorrect. Expected: '{expected_log_line}'"
        else:
            assert not user_in_log, f"Found unexpected alert for {user} who did not exceed quota."