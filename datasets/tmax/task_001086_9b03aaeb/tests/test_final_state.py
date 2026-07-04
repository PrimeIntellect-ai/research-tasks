# test_final_state.py
import os
import json
import pytest

def test_device_configs_generated():
    expected_configs = {
        "node-alpha_active.json": {
            "device_id": "node-alpha",
            "auth_token": "tk_9912a",
            "region": "EU",
            "telemetry": True
        },
        "node-beta_active.json": {
            "device_id": "node-beta",
            "auth_token": "tk_8821b",
            "region": "US",
            "telemetry": False
        },
        "node-gamma_active.json": {
            "device_id": "node-gamma",
            "auth_token": "tk_7734c",
            "region": "AP",
            "telemetry": True
        }
    }

    base_dir = "/home/user/device_configs"

    for filename, expected_content in expected_configs.items():
        filepath = os.path.join(base_dir, filename)
        assert os.path.isfile(filepath), f"Expected configuration file {filepath} was not generated."

        with open(filepath, 'r') as f:
            try:
                actual_content = json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"File {filepath} does not contain valid JSON.")

        assert actual_content == expected_content, f"Content of {filepath} does not match expected configuration. Expected {expected_content}, got {actual_content}."

def test_deploy_script_exists():
    script_path = "/home/user/deploy_fleet.py"
    assert os.path.isfile(script_path), f"Deployment script {script_path} is missing."