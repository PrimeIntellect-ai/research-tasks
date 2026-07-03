# test_final_state.py

import os
import subprocess
import re
import pytest

def test_cost_monitor_executable_exists():
    """Check that the compiled executable exists."""
    assert os.path.isfile("/home/user/cost_monitor"), "The executable /home/user/cost_monitor does not exist."
    assert os.access("/home/user/cost_monitor", os.X_OK), "/home/user/cost_monitor is not executable."

def test_cost_monitor_execution_with_env():
    """Check the output of the C++ program when FINOPS_TIER is set."""
    env = os.environ.copy()
    env["FINOPS_TIER"] = "premium"
    result = subprocess.run(["/home/user/cost_monitor"], env=env, capture_output=True, text=True)
    assert result.returncode == 0, "Execution of /home/user/cost_monitor failed."
    assert result.stdout.strip() == "[premium] Cost computation triggered.", f"Unexpected output: {result.stdout.strip()}"

def test_cost_monitor_execution_without_env():
    """Check the output of the C++ program when FINOPS_TIER is not set."""
    env = os.environ.copy()
    if "FINOPS_TIER" in env:
        del env["FINOPS_TIER"]
    result = subprocess.run(["/home/user/cost_monitor"], env=env, capture_output=True, text=True)
    assert result.returncode == 0, "Execution of /home/user/cost_monitor failed."
    assert result.stdout.strip() == "[standard] Cost computation triggered.", f"Unexpected output: {result.stdout.strip()}"

def test_bashrc_configuration():
    """Check that .bashrc contains the correct environment variables."""
    assert os.path.isfile("/home/user/.bashrc"), "/home/user/.bashrc does not exist."
    with open("/home/user/.bashrc", "r") as f:
        content = f.read()

    # Check TZ
    tz_pattern = r'export\s+TZ=[\'"]?Pacific/Auckland[\'"]?'
    assert re.search(tz_pattern, content), ".bashrc does not correctly export TZ=Pacific/Auckland."

    # Check FINOPS_TIER
    tier_pattern = r'export\s+FINOPS_TIER=[\'"]?enterprise[\'"]?'
    assert re.search(tier_pattern, content), ".bashrc does not correctly export FINOPS_TIER=enterprise."

def test_cron_verification():
    """Check that the cron_verify.txt file contains the correct cron expression."""
    assert os.path.isfile("/home/user/cron_verify.txt"), "/home/user/cron_verify.txt does not exist."
    with open("/home/user/cron_verify.txt", "r") as f:
        content = f.read()

    # Match 45 23 * * * /home/user/cost_monitor with flexible spacing
    cron_pattern = r'^45\s+23\s+\*\s+\*\s+\*\s+/home/user/cost_monitor\b'

    found = False
    for line in content.splitlines():
        if re.search(cron_pattern, line.strip()):
            found = True
            break

    assert found, "cron_verify.txt does not contain the correct cron expression for /home/user/cost_monitor."