# test_final_state.py

import os
import json
import pytest

def test_security_alerts_log():
    log_path = '/home/user/output/security_alerts.log'
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_paths = [
        "../db_secret.json",
        "../../web_secret.json",
        "/etc/shadow",
        "folder/../../etc/passwd"
    ]

    # The task requires the output to be sorted alphabetically.
    # We will check both the content and the sorting.
    assert sorted(lines) == sorted(expected_paths), "The logged malicious paths do not match the expected paths."
    assert lines == sorted(lines), "The malicious paths in the log file are not sorted alphabetically as requested."

def test_merged_configs_json():
    json_path = '/home/user/output/merged_configs.json'
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert isinstance(data, list), "The merged configuration should be a JSON array."

    expected_data = [
        {
            "service": "db",
            "version": "1.0",
            "settings": {
                "port": 5432
            }
        },
        {
            "service": "web",
            "version": "2.1",
            "settings": {
                "host": "localhost",
                "tls": True
            }
        }
    ]

    # Check if the data matches the expected data
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} merged configs, found {len(data)}."

    # The task requires the array to be sorted alphabetically by the 'service' string.
    services = [item.get('service', '') for item in data]
    assert services == sorted(services), "The merged JSON array is not sorted alphabetically by the 'service' string."

    # Sort both just in case, to check content equality
    sorted_data = sorted(data, key=lambda x: x.get('service', ''))
    sorted_expected = sorted(expected_data, key=lambda x: x.get('service', ''))

    assert sorted_data == sorted_expected, "The merged configuration content does not match the expected valid configurations."