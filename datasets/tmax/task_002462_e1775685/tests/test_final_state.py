# test_final_state.py
import os
import json
import pytest

ACTIVE_CONFIGS_DIR = "/home/user/active_configs"
INVENTORY_FILE = "/home/user/config_inventory.json"

def test_active_configs_dir_exists():
    assert os.path.isdir(ACTIVE_CONFIGS_DIR), f"Directory {ACTIVE_CONFIGS_DIR} does not exist."

def test_active_configs_files():
    expected_files = {
        "auth_service_1.5.2.json": {
            "app_name": "Auth Service",
            "config_version": "1.5.2",
            "settings": {"retry": 3}
        },
        "payment_gateway_3.0.json": {
            "app_name": "Payment_Gateway",
            "config_version": "3.0",
            "settings": {"timeout": 30}
        }
    }

    actual_files = set(os.listdir(ACTIVE_CONFIGS_DIR))
    expected_filenames = set(expected_files.keys())

    missing = expected_filenames - actual_files
    assert not missing, f"Missing expected files in {ACTIVE_CONFIGS_DIR}: {missing}"

    extra = actual_files - expected_filenames
    assert not extra, f"Unexpected files found in {ACTIVE_CONFIGS_DIR}: {extra}"

    for filename, expected_content in expected_files.items():
        filepath = os.path.join(ACTIVE_CONFIGS_DIR, filename)
        with open(filepath, 'r') as f:
            try:
                content = json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"File {filepath} is not valid JSON.")

        assert content == expected_content, f"Content of {filename} does not match the original."

def test_inventory_file_exists_and_content():
    assert os.path.isfile(INVENTORY_FILE), f"Inventory file {INVENTORY_FILE} does not exist."

    with open(INVENTORY_FILE, 'r') as f:
        try:
            inventory = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Inventory file {INVENTORY_FILE} is not valid JSON.")

    expected_inventory = {
        "auth_service": "1.5.2",
        "payment_gateway": "3.0"
    }

    assert inventory == expected_inventory, f"Inventory content {inventory} does not match expected {expected_inventory}."