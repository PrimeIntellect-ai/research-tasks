# test_final_state.py

import os
import json
import pytest

OUTPUT_FILE = "/home/user/processed_logs.jsonl"

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"The output file {OUTPUT_FILE} was not created."
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a file."

def test_output_file_contents():
    with open(OUTPUT_FILE, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 4, f"Expected 4 lines in {OUTPUT_FILE}, found {len(lines)}."

    expected_data = [
        {
            "timestamp": "2023-10-12T14:32:01Z",
            "method": "GET",
            "path": "/api/v1/users",
            "status": 200,
            "bytes": 1024,
            "ip": "192.168.1.XXX",
            "pii_detected": {
                "emails": ["a*****@example.com"],
                "credit_cards": [],
                "ssns": []
            }
        },
        {
            "timestamp": "2023-10-12T14:35:10Z",
            "method": "POST",
            "path": "/api/v1/payments",
            "status": 201,
            "bytes": 512,
            "ip": "10.0.0.XXX",
            "pii_detected": {
                "emails": ["b*****@domain.co.uk"],
                "credit_cards": ["XXXX-XXXX-XXXX-3456"],
                "ssns": []
            }
        },
        {
            "timestamp": "2023-10-13T09:15:00Z",
            "method": "PUT",
            "path": "/secure/vault/data",
            "status": 403,
            "bytes": 0,
            "ip": "172.16.254.XXX",
            "pii_detected": {
                "emails": ["c*****@hackers.org"],
                "credit_cards": [],
                "ssns": ["XXX-XX-7777"]
            }
        },
        {
            "timestamp": "2023-10-14T00:00:01Z",
            "method": "GET",
            "path": "/health_check",
            "status": 200,
            "bytes": 42,
            "ip": "127.0.0.XXX",
            "pii_detected": {
                "emails": [],
                "credit_cards": [],
                "ssns": []
            }
        }
    ]

    for i, line in enumerate(lines):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {OUTPUT_FILE} is not valid JSON.")

        expected = expected_data[i]

        assert parsed.get("timestamp") == expected["timestamp"], f"Line {i+1} timestamp mismatch."
        assert parsed.get("method") == expected["method"], f"Line {i+1} method mismatch."
        assert parsed.get("path") == expected["path"], f"Line {i+1} path mismatch."
        assert parsed.get("status") == expected["status"], f"Line {i+1} status mismatch."
        assert parsed.get("bytes") == expected["bytes"], f"Line {i+1} bytes mismatch."
        assert parsed.get("ip") == expected["ip"], f"Line {i+1} ip mismatch."

        pii = parsed.get("pii_detected", {})
        assert isinstance(pii, dict), f"Line {i+1} pii_detected is not a dictionary."

        assert set(pii.get("emails", [])) == set(expected["pii_detected"]["emails"]), f"Line {i+1} emails mismatch."
        assert set(pii.get("credit_cards", [])) == set(expected["pii_detected"]["credit_cards"]), f"Line {i+1} credit_cards mismatch."
        assert set(pii.get("ssns", [])) == set(expected["pii_detected"]["ssns"]), f"Line {i+1} ssns mismatch."