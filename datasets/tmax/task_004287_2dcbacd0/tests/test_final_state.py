# test_final_state.py

import os
import json
import pytest

MANIFESTS_DIR = "/home/user/manifests"
PROXY_CONFIG_PATH = "/home/user/proxy_config.json"
LOG_PATH = "/home/user/operator.log"

def compute_expected_state():
    if not os.path.isdir(MANIFESTS_DIR):
        return {}, [], []

    files = sorted(os.listdir(MANIFESTS_DIR))
    config = {}
    json_errors = []
    schema_errors = []

    for filename in files:
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(MANIFESTS_DIR, filename)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            json_errors.append(filename)
            continue

        if not isinstance(data, dict):
            schema_errors.append(filename)
            continue

        if set(data.keys()) != {"route", "target_port", "allowed_ips"}:
            schema_errors.append(filename)
            continue

        if (not isinstance(data["route"], str) or 
            not isinstance(data["target_port"], int) or 
            not isinstance(data["allowed_ips"], list) or 
            not all(isinstance(ip, str) for ip in data["allowed_ips"])):
            schema_errors.append(filename)
            continue

        config[data["route"]] = {
            "target_port": data["target_port"],
            "allowed_ips": data["allowed_ips"]
        }

    return config, json_errors, schema_errors

def test_proxy_config_exists_and_correct():
    assert os.path.isfile(PROXY_CONFIG_PATH), f"Expected configuration file {PROXY_CONFIG_PATH} does not exist."

    with open(PROXY_CONFIG_PATH, 'r') as f:
        try:
            actual_config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {PROXY_CONFIG_PATH} is not valid JSON.")

    expected_config, _, _ = compute_expected_state()
    assert actual_config == expected_config, f"Contents of {PROXY_CONFIG_PATH} do not match the expected configuration."

def test_operator_log_correct():
    assert os.path.isfile(LOG_PATH), f"Expected log file {LOG_PATH} does not exist."

    with open(LOG_PATH, 'r') as f:
        log_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(log_lines) > 0, f"Log file {LOG_PATH} is empty."
    assert log_lines[0] == "OPERATOR RUN STARTED", "Log file must start with 'OPERATOR RUN STARTED'."
    assert log_lines[-1] == "OPERATOR RUN COMPLETED", "Log file must end with 'OPERATOR RUN COMPLETED'."

    expected_config, json_errors, schema_errors = compute_expected_state()

    middle_lines = log_lines[1:-1]

    for err_file in json_errors:
        expected_err = f"ERROR: Invalid JSON in {err_file}"
        assert expected_err in middle_lines, f"Missing expected error log for JSON decode failure: {expected_err}"

    for err_file in schema_errors:
        expected_err = f"ERROR: Invalid schema in {err_file}"
        assert expected_err in middle_lines, f"Missing expected error log for schema validation failure: {expected_err}"

    success_lines = [line for line in middle_lines if line.startswith("SUCCESS:")]
    expected_success_lines = []
    for route in sorted(expected_config.keys()):
        port = expected_config[route]["target_port"]
        expected_success_lines.append(f"SUCCESS: Configured route {route} to port {port}")

    assert success_lines == expected_success_lines, "SUCCESS log lines are either incorrect or not in alphabetical order by route."