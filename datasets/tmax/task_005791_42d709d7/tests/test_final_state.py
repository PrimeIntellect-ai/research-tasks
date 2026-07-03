# test_final_state.py
import os
import pytest

def test_investigation_report_exists():
    """Verify that the investigation report file was created."""
    assert os.path.isfile('/home/user/investigation_report.txt'), "The file /home/user/investigation_report.txt is missing."

def test_investigation_report_content():
    """Verify the contents of the investigation report."""
    with open('/home/user/investigation_report.txt', 'r') as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split('\n') if line.strip()]

    expected_dict = {
        "Port": "8233",
        "Cookie": "AuthToken=Tr0j4n99",
        "CustomHeader": "X-C2-Auth: Active",
        "Payload": "EICAR_OR_SIMILAR_MALWARE_STRING",
        "Malicious_IPs": "198.51.100.45,203.0.113.88"
    }

    actual_dict = {}
    for line in lines:
        if ':' in line:
            # Split by the first colon to handle CustomHeader correctly
            key, val = line.split(':', 1)
            actual_dict[key.strip()] = val.strip()

    for key, expected_value in expected_dict.items():
        actual_value = actual_dict.get(key)
        assert actual_value is not None, f"Missing key '{key}' in the report."
        assert actual_value == expected_value, f"Incorrect value for '{key}'. Expected '{expected_value}', but got '{actual_value}'."