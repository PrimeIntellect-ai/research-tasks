# test_final_state.py

import os
import json
import pytest

DESIRED_STATE_FILE = "/home/user/desired_state.json"
OPERATOR_SCRIPT = "/home/user/manifest_operator.py"
LOGROTATE_CONF = "/home/user/generated_logrotate.conf"

def get_desired_state():
    assert os.path.isfile(DESIRED_STATE_FILE), f"Missing {DESIRED_STATE_FILE}"
    with open(DESIRED_STATE_FILE, "r") as f:
        return json.load(f)

def test_operator_script_exists():
    """Verify that the manifest operator script exists."""
    assert os.path.isfile(OPERATOR_SCRIPT), f"The script {OPERATOR_SCRIPT} does not exist."

def test_log_directories_exist():
    """Verify that the log directories specified in the desired state exist."""
    state = get_desired_state()
    containers = state.get("containers", [])
    assert containers, "No containers found in desired state."

    for container in containers:
        log_dir = container.get("log_dir")
        assert log_dir, f"Container {container.get('name')} is missing a log_dir."
        assert os.path.isdir(log_dir), f"The expected log directory {log_dir} does not exist."

def test_logrotate_conf_content():
    """Verify that the generated logrotate configuration matches the expected output."""
    assert os.path.isfile(LOGROTATE_CONF), f"The file {LOGROTATE_CONF} does not exist."

    state = get_desired_state()
    containers = state.get("containers", [])

    expected_blocks = []
    for container in containers:
        log_dir = container.get("log_dir")
        block = f"{log_dir}/*.log {{\n    daily\n    rotate 7\n    compress\n    missingok\n    notifempty\n}}"
        expected_blocks.append(block)

    expected_content = "\n\n".join(expected_blocks)

    with open(LOGROTATE_CONF, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"The content of {LOGROTATE_CONF} does not match the expected format."