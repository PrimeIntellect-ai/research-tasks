# test_final_state.py
import os
import json

def test_output_jsonl_exists():
    """Test that the output.jsonl file was created."""
    file_path = "/home/user/output.jsonl"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

def test_output_jsonl_content():
    """Test that the output.jsonl contains the correct JSON objects."""
    file_path = "/home/user/output.jsonl"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

    expected_records = [
        {"device_id": "D1", "timestamp": "2", "temp_avg": "21.00", "distance": "2.24"},
        {"device_id": "D2", "timestamp": "5", "temp_avg": "20.00", "distance": "2.24"},
        {"device_id": "D1", "timestamp": "6", "temp_avg": "23.00", "distance": "3.00"},
        {"device_id": "D2", "timestamp": "8", "temp_avg": "21.00", "distance": "2.24"}
    ]

    actual_records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_records.append(record)
            except json.JSONDecodeError as e:
                assert False, f"Line {line_num} in {file_path} is not valid JSON: {e}"

    assert len(actual_records) == len(expected_records), (
        f"Expected {len(expected_records)} records in {file_path}, but found {len(actual_records)}."
    )

    # We sort both lists of dictionaries to ensure order doesn't fail the test
    # (though streaming usually implies arrival order)
    def sort_key(r):
        return (r.get("device_id", ""), int(r.get("timestamp", "0")))

    actual_records_sorted = sorted(actual_records, key=sort_key)
    expected_records_sorted = sorted(expected_records, key=sort_key)

    for i, (actual, expected) in enumerate(zip(actual_records_sorted, expected_records_sorted)):
        assert actual == expected, (
            f"Record mismatch at sorted index {i}.\n"
            f"Expected: {expected}\n"
            f"Actual: {actual}"
        )