# test_final_state.py

import os
import pytest

OBS_STACK_DIR = "/home/user/obs_stack"
DASHBOARD_LOG = os.path.join(OBS_STACK_DIR, "dashboard.log")
AGGREGATOR_BIN = os.path.join(OBS_STACK_DIR, "aggregator")
START_SH = os.path.join(OBS_STACK_DIR, "start.sh")

def test_dashboard_log_exists():
    assert os.path.isfile(DASHBOARD_LOG), f"File {DASHBOARD_LOG} was not created. The start.sh script or aggregator failed."

def test_dashboard_log_content():
    with open(DASHBOARD_LOG, "r") as f:
        content = f.read().strip()
    expected = "[SUCCESS] Metrics received: cpu_usage=42% mem_usage=60%"
    assert expected in content, f"Content of {DASHBOARD_LOG} is incorrect. Expected to contain '{expected}', but got '{content}'."

def test_aggregator_binary_exists():
    assert os.path.isfile(AGGREGATOR_BIN), f"Compiled executable {AGGREGATOR_BIN} does not exist."
    assert os.access(AGGREGATOR_BIN, os.X_OK), f"File {AGGREGATOR_BIN} is not executable."

def test_start_sh_contains_socat():
    with open(START_SH, "r") as f:
        content = f.read()
    assert "socat" in content, "start.sh does not appear to use 'socat' for port forwarding as requested."