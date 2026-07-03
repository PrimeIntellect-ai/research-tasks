# test_final_state.py

import os
import json
import requests
import subprocess
import pytest

def get_legacy_hash(user_id: str) -> str:
    try:
        result = subprocess.check_output(["/app/legacy_hasher", user_id], text=True)
        return result.strip()
    except Exception as e:
        pytest.fail(f"Failed to execute /app/legacy_hasher for user_id {user_id}: {e}")

def test_etl_stream_processing():
    url = "http://127.0.0.1:9090/api/v1/process"

    # Input data
    input_records = [
        {"user_id": "101", "email": "alice@example.com", "event": "click"},
        {"user_id": "102", "email": "bob@example.com", "event": "view"},
        {"user_id": "103", "email": "charlie@example.com", "event": "purchase"},
        {"user_id": "104", "email": "dave@example.com", "event": "login"}
    ]

    payload = "\n".join(json.dumps(record) for record in input_records)

    # Determine expected output dynamically using the binary
    expected_output_records = []
    for record in input_records:
        secure_token = get_legacy_hash(record["user_id"])
        if secure_token and secure_token[0].lower() in "abcdef":
            expected_record = record.copy()
            expected_record["email"] = "***@***.***"
            expected_record["secure_token"] = secure_token
            expected_output_records.append(expected_record)

    try:
        response = requests.post(url, data=payload, headers={"Content-Type": "application/x-ndjson"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the ETL server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    # Parse response
    response_lines = [line.strip() for line in response.text.strip().split("\n") if line.strip()]
    response_records = []
    for line in response_lines:
        try:
            response_records.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Server returned invalid JSONL: {line}")

    assert len(response_records) == len(expected_output_records), (
        f"Expected {len(expected_output_records)} retained records, but got {len(response_records)}."
    )

    for expected, actual in zip(expected_output_records, response_records):
        assert actual == expected, f"Mismatch in record.\nExpected: {expected}\nActual: {actual}"

def test_etl_metrics_log():
    log_path = "/home/user/etl_metrics.log"
    assert os.path.exists(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) > 0, "Log file is empty."
    last_line = lines[-1]

    # We sent 4 records in the previous test. Let's verify the format.
    # The actual numbers might depend on whether the test is run isolated or not,
    # but the format must be exact.
    assert last_line.startswith("PROCESSED:"), f"Log line does not start with 'PROCESSED:'. Line: {last_line}"
    assert "|RETAINED:" in last_line, f"Log line does not contain '|RETAINED:'. Line: {last_line}"

    parts = last_line.split("|")
    assert len(parts) == 2, f"Log line format invalid: {last_line}"

    processed_part = parts[0].split(":")
    retained_part = parts[1].split(":")

    assert len(processed_part) == 2 and processed_part[1].isdigit(), f"Invalid PROCESSED count: {last_line}"
    assert len(retained_part) == 2 and retained_part[1].isdigit(), f"Invalid RETAINED count: {last_line}"