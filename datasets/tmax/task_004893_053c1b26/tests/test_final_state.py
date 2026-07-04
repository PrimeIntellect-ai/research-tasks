# test_final_state.py

import os
import json
import pytest

def str_dict(d):
    """Recursively convert all values in a dictionary to strings for safe comparison."""
    if isinstance(d, dict):
        return {k: str_dict(v) for k, v in d.items()}
    return str(d)

def test_final_configs_exists():
    path = '/home/user/final_configs.json'
    assert os.path.isfile(path), f"Output file {path} does not exist."

def test_final_configs_valid_json():
    path = '/home/user/final_configs.json'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to parse {path} as JSON. Error: {e}")

def test_final_configs_content():
    path = '/home/user/final_configs.json'
    with open(path, 'r', encoding='utf-8') as f:
        result = json.load(f)

    expected = {
      "device_alpha": {
        "network_speed": "10000",
        "duplex": "full",
        "mtu": "1500"
      },
      "device_beta": {
        "timeout": "60",
        "retries": "3",
        "mode": "active"
      },
      "device_gamma": {
        "power_limit": "200W",
        "fan_curve": "aggressive",
        "led_mode": "breathing"
      }
    }

    assert str_dict(result) == str_dict(expected), (
        "Output JSON does not match the expected consolidated state. "
        "Ensure you are extracting the latest values based on timestamps."
    )