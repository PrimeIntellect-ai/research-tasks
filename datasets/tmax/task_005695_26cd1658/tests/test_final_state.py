# test_final_state.py
import os
import json
import pytest

def test_billing_status_exists_and_correct():
    status_file = '/home/user/billing_status.json'
    assert os.path.exists(status_file), f"The output file {status_file} does not exist. The ingestion pipeline did not complete successfully."

    with open(status_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {status_file} is not valid JSON.")

    expected = {
        "status": "success",
        "secret_used": "zk99_fX82_legacy_auth_key",
        "customer": "AcmeCorp",
        "amount": 10500
    }

    assert data == expected, f"The contents of {status_file} do not match the expected output. Found: {data}"