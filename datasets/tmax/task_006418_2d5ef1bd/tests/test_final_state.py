# test_final_state.py
import os
import json
import pytest

OUTPUT_PATH = '/home/user/clean_logs.jsonl'

@pytest.fixture
def clean_logs():
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."
    assert os.path.isfile(OUTPUT_PATH), f"Path {OUTPUT_PATH} is not a file."

    data = []
    with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                pytest.fail(f"Could not parse line {line_num} as JSON: {e}")
    return data

def test_record_count(clean_logs):
    assert len(clean_logs) == 7, f"Expected exactly 7 records, got {len(clean_logs)}"

def test_chronological_sorting(clean_logs):
    timestamps = [record.get("ts") for record in clean_logs]
    assert all(timestamps[i] <= timestamps[i+1] for i in range(len(timestamps)-1)), "Records are not sorted chronologically by 'ts'."

def test_expected_data_content(clean_logs):
    expected_data = [
        {"ts": "2023-05-12T14:00:00Z", "user_id": "u1", "message": "hello from ***@***.***"},
        {"ts": "2023-05-12T14:01:00Z", "user_id": "u2", "message": "testing \ud83d\ude00"},
        {"ts": "2023-05-12T14:02:00Z", "user_id": "unknown", "message": "imputed"},
        {"ts": "2023-05-12T14:03:00Z", "user_id": "u3", "message": "reach out to ***@***.***."},
        {"ts": "2023-05-12T14:04:00Z", "user_id": "unknown", "message": "imputed"},
        {"ts": "2023-05-12T14:05:00Z", "user_id": "u1", "message": "skip ahead"},
        {"ts": "2023-05-12T14:06:00Z", "user_id": "u4", "message": "bad escape  here"}
    ]

    assert len(clean_logs) == len(expected_data), f"Expected {len(expected_data)} records, got {len(clean_logs)}"

    for i, (actual, expected) in enumerate(zip(clean_logs, expected_data)):
        assert actual.get("ts") == expected["ts"], f"Record {i} timestamp mismatch. Expected {expected['ts']}, got {actual.get('ts')}"
        assert actual.get("user_id") == expected["user_id"], f"Record {i} user_id mismatch. Expected {expected['user_id']}, got {actual.get('user_id')}"
        assert actual.get("message") == expected["message"], f"Record {i} message mismatch. Expected {expected['message']}, got {actual.get('message')}"