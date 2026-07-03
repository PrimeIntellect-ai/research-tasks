# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/check_deploy.py"
JSON_PATH = "/home/user/deploy_status.json"
BASHRC_PATH = "/home/user/.bashrc"
TZ_LINE = "export TZ=Asia/Tokyo"
CRON_LINE = "*/5 * * * * /usr/bin/python3 /home/user/check_deploy.py"

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_json_output():
    assert os.path.isfile(JSON_PATH), f"JSON output file {JSON_PATH} does not exist."
    with open(JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} does not contain valid JSON.")

    assert data.get("stage1") == "offline", "stage1 should be 'offline'"
    assert data.get("stage2") == "offline", "stage2 should be 'offline'"
    assert data.get("last_checked_tz") == "Asia/Tokyo", "last_checked_tz should be 'Asia/Tokyo'"

def test_bashrc_updated():
    assert os.path.isfile(BASHRC_PATH), f"{BASHRC_PATH} does not exist."
    with open(BASHRC_PATH, "r") as f:
        content = f.read()

    count = content.splitlines().count(TZ_LINE)
    assert count >= 1, f"Could not find '{TZ_LINE}' in {BASHRC_PATH}."

def test_crontab_updated():
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read crontab: {e.output}")

    count = output.splitlines().count(CRON_LINE)
    assert count >= 1, f"Could not find '{CRON_LINE}' in crontab."

def test_idempotency():
    # Run the script again to test idempotency
    try:
        subprocess.check_call(["/usr/bin/python3", SCRIPT_PATH])
    except subprocess.CalledProcessError:
        pytest.fail(f"Execution of {SCRIPT_PATH} failed during idempotency check.")

    # Check bashrc again
    with open(BASHRC_PATH, "r") as f:
        content = f.read()
    count = content.splitlines().count(TZ_LINE)
    assert count == 1, f"Idempotency failed: found {count} occurrences of '{TZ_LINE}' in {BASHRC_PATH}."

    # Check crontab again
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read crontab: {e.output}")

    count = output.splitlines().count(CRON_LINE)
    assert count == 1, f"Idempotency failed: found {count} occurrences of '{CRON_LINE}' in crontab."