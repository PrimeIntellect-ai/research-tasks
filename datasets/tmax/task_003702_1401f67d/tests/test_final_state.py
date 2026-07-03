# test_final_state.py

import os
import csv
import json
import hashlib
import pytest

def get_expected_data():
    input_file = "/home/user/raw_logs.json"
    assert os.path.exists(input_file), f"Input file {input_file} is missing."

    with open(input_file, "r") as f:
        data = json.load(f)

    expected_rows = []
    for session in data:
        client_ip = session.get("client_ip", "")
        user_id = session.get("user_id", "")

        # Mask IP
        if "." in client_ip:
            ip_parts = client_ip.split(".")
            ip_parts[-1] = "0"
            masked_ip = ".".join(ip_parts)
        else:
            masked_ip = client_ip

        # Anonymize user_id
        anonymized_user_id = hashlib.sha256(user_id.encode('utf-8')).hexdigest()

        for event in session.get("events", []):
            timestamp = event.get("timestamp", "")
            event_type = event.get("event_type", "")
            request = event.get("request", "")

            # Parse request
            parts = request.split()
            if len(parts) >= 2:
                method = parts[0]
                raw_path = parts[1]

                # Normalize path
                path_segments = raw_path.split("/")
                norm_segments = ["{id}" if seg.isdigit() else seg for seg in path_segments]
                normalized_path = "/".join(norm_segments)
            else:
                method = "UNKNOWN"
                normalized_path = "UNKNOWN"

            expected_rows.append([
                timestamp,
                event_type,
                method,
                normalized_path,
                masked_ip,
                anonymized_user_id
            ])

    # Sort by timestamp ascending
    expected_rows.sort(key=lambda x: x[0])
    return expected_rows

def test_processed_logs_csv_exists():
    """Test that the processed_logs.csv file was created."""
    file_path = "/home/user/processed_logs.csv"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_processed_logs_content():
    """Test that the CSV content matches the expected ETL output."""
    file_path = "/home/user/processed_logs.csv"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    expected_rows = get_expected_data()
    expected_headers = ["timestamp", "event_type", "method", "normalized_path", "masked_ip", "anonymized_user_id"]

    with open(file_path, "r", newline="") as f:
        reader = csv.reader(f)
        actual_data = list(reader)

    assert len(actual_data) > 0, "The CSV file is empty."

    actual_headers = actual_data[0]
    assert actual_headers == expected_headers, f"CSV headers are incorrect. Expected {expected_headers}, got {actual_headers}"

    actual_rows = actual_data[1:]
    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch.\nExpected: {expected}\nGot: {actual}"