# test_final_state.py

import os
import re
import stat
import json
import subprocess
import shutil
import pytest

SERVICE_FILE = "/home/user/optimizer.service"
SCRIPT_FILE = "/home/user/cost_optimizer.py"
CONFIG_FILE = "/home/user/port_mapping.json"
OUTPUT_FILE = "/home/user/apply_port_rules.sh"

def test_systemd_service_configured():
    assert os.path.isfile(SERVICE_FILE), f"Service file {SERVICE_FILE} is missing."
    with open(SERVICE_FILE, "r") as f:
        content = f.read()

    assert re.search(r"^After=.*billing-api\.service", content, re.MULTILINE), \
        "optimizer.service does not contain the correct 'After=billing-api.service' directive."

    assert re.search(r"^ExecStart=.*python3\s+/home/user/cost_optimizer\.py", content, re.MULTILINE), \
        "optimizer.service does not contain the correct 'ExecStart' directive calling cost_optimizer.py with python3."

def test_python_script_exists():
    assert os.path.isfile(SCRIPT_FILE), f"Python script {SCRIPT_FILE} is missing."

def test_execution_business_hours():
    # 2023-10-10 16:00:00 UTC is 12:00 PM EDT (New York) -> Business hours
    env = os.environ.copy()
    env["TZ"] = "UTC"

    # Remove output file if it exists to ensure we check the new run
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    result = subprocess.run(
        ["faketime", "2023-10-10 16:00:00", "python3", SCRIPT_FILE],
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed during business hours execution: {result.stderr}"
    assert os.path.isfile(OUTPUT_FILE), f"Output script {OUTPUT_FILE} was not created."

    with open(OUTPUT_FILE, "r") as f:
        content = f.read()

    assert "socat TCP4-LISTEN:5432,bind=127.0.0.1,fork TCP4:127.0.0.1:15432 &" in content, \
        "Missing or incorrect socat command for 'db' during business hours."
    assert "socat TCP4-LISTEN:6379,bind=127.0.0.1,fork TCP4:127.0.0.1:16379 &" in content, \
        "Missing or incorrect socat command for 'cache' during business hours."

    # Check permissions strictly 700
    st = os.stat(OUTPUT_FILE)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Permissions for {OUTPUT_FILE} should be 700, but got {oct(perms)}."

def test_execution_off_hours():
    # 2023-10-10 04:00:00 UTC is 00:00 AM EDT (New York) -> Off hours
    env = os.environ.copy()
    env["TZ"] = "UTC"

    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    result = subprocess.run(
        ["faketime", "2023-10-10 04:00:00", "python3", SCRIPT_FILE],
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed during off hours execution: {result.stderr}"
    assert os.path.isfile(OUTPUT_FILE), f"Output script {OUTPUT_FILE} was not created."

    with open(OUTPUT_FILE, "r") as f:
        content = f.read()

    assert 'echo "Off-hours: tunnels disabled"' in content, \
        "Output script does not contain the correct off-hours message."

def test_execution_missing_config():
    backup_file = f"{CONFIG_FILE}.bak"
    if os.path.exists(CONFIG_FILE):
        shutil.move(CONFIG_FILE, backup_file)

    try:
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)

        result = subprocess.run(
            ["python3", SCRIPT_FILE],
            capture_output=True,
            text=True
        )
        # We don't assert return code here strictly, as long as it handles the error by writing the file
        assert os.path.isfile(OUTPUT_FILE), f"Output script {OUTPUT_FILE} was not created when config is missing."

        with open(OUTPUT_FILE, "r") as f:
            content = f.read()

        assert 'echo "Error: missing config"' in content, \
            "Output script does not contain the correct error message when config is missing."
    finally:
        if os.path.exists(backup_file):
            shutil.move(backup_file, CONFIG_FILE)