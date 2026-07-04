# test_final_state.py

import os
import json
import pytest

def test_proxy_config_exists():
    file_path = "/home/user/proxy_config.json"
    assert os.path.isfile(file_path), f"The file {file_path} is missing. The Go program might not have generated it."

def test_proxy_config_content():
    file_path = "/home/user/proxy_config.json"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    expected_config = {
        "DB": "http://localhost:8000",
        "Analytics": "http://localhost:8001",
        "Auth": "http://localhost:8002",
        "Ledger": "http://localhost:8003",
        "Notification": "http://localhost:8004",
        "Payment": "http://localhost:8005"
    }

    assert config == expected_config, f"The content of {file_path} does not match the expected topological sort and port assignment."