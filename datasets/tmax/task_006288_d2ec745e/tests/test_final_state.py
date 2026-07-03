# test_final_state.py
import os
import json
import csv

def test_invalid_records_jsonl():
    invalid_file = "/home/user/invalid_records.jsonl"
    assert os.path.exists(invalid_file), f"File {invalid_file} is missing."
    assert os.path.isfile(invalid_file), f"Path {invalid_file} is not a file."

    expected_invalid = [
        {"user_id": 102, "ad_id": 502, "clicks": "2", "impressions": 50, "timestamp": "2023-10-15T09:15:00Z"},
        {"user_id": 103, "ad_id": 503, "clicks": 10, "impressions": 5, "timestamp": "2023-10-15T14:00:00Z"},
        {"user_id": 101, "ad_id": 506, "clicks": -1, "impressions": 10, "timestamp": "2023-10-15T08:30:00Z"},
        {"user_id": 106, "ad_id": 507, "clicks": 2, "impressions": 0, "timestamp": "2023-10-15T11:00:00Z"},
        {"user_id": 107, "ad_id": 508, "clicks": 3, "impressions": 50},
        {"user_id": 108, "ad_id": 509, "clicks": 15, "impressions": 1000, "timestamp": "2023-10-15T18:22:00Z", "extra_field": True}
    ]

    with open(invalid_file, "r") as f:
        lines = f.read().strip().split('\n')

    actual_invalid = []
    for line in lines:
        if not line.strip():
            continue
        try:
            actual_invalid.append(json.loads(line))
        except json.JSONDecodeError:
            assert False, f"Line in {invalid_file} is not valid JSON: {line}"

    # Order doesn't strictly matter
    assert len(actual_invalid) == len(expected_invalid), f"Expected {len(expected_invalid)} invalid records, found {len(actual_invalid)}"

    for expected_record in expected_invalid:
        assert expected_record in actual_invalid, f"Expected invalid record {expected_record} not found in {invalid_file}"


def test_processed_data_csv():
    processed_file = "/home/user/processed_data.csv"
    assert os.path.exists(processed_file), f"File {processed_file} is missing."
    assert os.path.isfile(processed_file), f"Path {processed_file} is not a file."

    expected_header = ["user_id", "ad_id", "hour_of_day", "clicks", "impressions", "bayesian_ctr"]
    expected_rows = [
        ["101", "501", "8", "5", "100", "0.0347"],
        ["104", "504", "22", "0", "20", "0.0164"],
        ["105", "505", "0", "1", "10", "0.0268"],
        ["109", "510", "18", "15", "1000", "0.0154"]
    ]

    with open(processed_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{processed_file} is empty."

    actual_header = rows[0]
    assert actual_header == expected_header, f"Expected header {expected_header}, found {actual_header}"

    actual_data = rows[1:]
    assert len(actual_data) == len(expected_rows), f"Expected {len(expected_rows)} processed records, found {len(actual_data)}"

    for i, (actual_row, expected_row) in enumerate(zip(actual_data, expected_rows)):
        assert actual_row == expected_row, f"Row {i+1} mismatch. Expected {expected_row}, found {actual_row}. Make sure data is sorted by user_id then ad_id."