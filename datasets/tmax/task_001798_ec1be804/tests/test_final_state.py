# test_final_state.py
import os
import json

def test_go_script_exists():
    go_path = "/home/user/process_dataset.go"
    assert os.path.exists(go_path), f"The Go program {go_path} is missing."
    assert os.path.isfile(go_path), f"{go_path} should be a file."

def test_valid_records_jsonl():
    output_jsonl = "/home/user/valid_records.jsonl"
    assert os.path.exists(output_jsonl), f"The output file {output_jsonl} is missing."
    assert os.path.isfile(output_jsonl), f"{output_jsonl} should be a file."

    expected_records = [
        {"id": "A1", "status": "valid", "value": 10.5},
        {"id": "A3", "status": "valid", "value": 42.1},
        {"id": "B2", "status": "valid", "value": 99.9},
        {"id": "C1", "status": "valid", "value": 3.14},
        {"id": "C2", "status": "valid", "value": 2.71}
    ]

    actual_records = []
    with open(output_jsonl, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_records.append(record)
            except json.JSONDecodeError:
                assert False, f"Line {line_num} in {output_jsonl} is not valid JSON: {line}"

    assert len(actual_records) == len(expected_records), f"Expected {len(expected_records)} valid records, but found {len(actual_records)}."

    # Compare independent of order
    def sort_key(record):
        return record.get("id", "")

    expected_sorted = sorted(expected_records, key=sort_key)
    actual_sorted = sorted(actual_records, key=sort_key)

    assert actual_sorted == expected_sorted, f"The records in {output_jsonl} do not match the expected valid records."