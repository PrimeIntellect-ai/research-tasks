# test_final_state.py

import os
import json
import subprocess

def compute_embedding(text):
    length = len(text)
    vowels = sum(1 for c in text.lower() if c in 'aeiou')
    consonants = sum(1 for c in text.lower() if c in 'bcdfghjklmnpqrstvwxyz')
    return [length, vowels, consonants]

def get_expected_data():
    raw_data = [
        {"id": 10, "text": "Great product", "label": "POSITIVE"},
        {"id": 15, "text": "Terrible experience", "label": "NEGATIVE"},
        {"id": "2", "text": "String ID invalid", "label": "POSITIVE"},
        {"id": 8, "text": "Missing label"},
        {"id": 3, "text": "Okay", "label": "NEUTRAL"},
        {"id": 12, "text": "Loved it", "label": "POSITIVE"},
        {"id": 5, "text": "Not bad", "label": "POSITIVE"},
        {"id": 20, "text": "Worst thing ever", "label": "NEGATIVE"},
        {"id": 1, "text": "Awesome", "label": "POSITIVE"},
        {"id": 7, "text": "Hated it", "label": "NEGATIVE"},
        {"id": 25, "text": 12345, "label": "POSITIVE"}
    ]

    valid_records = []
    for record in raw_data:
        if "id" in record and isinstance(record["id"], (int, float)) and not isinstance(record["id"], bool):
            if "text" in record and isinstance(record["text"], str):
                if "label" in record and record["label"] in ["POSITIVE", "NEGATIVE"]:
                    valid_records.append(record)

    valid_records.sort(key=lambda x: x["id"])
    top_5 = valid_records[:5]

    expected = []
    for record in top_5:
        r = record.copy()
        r["embedding"] = compute_embedding(r["text"])
        expected.append(r)

    return expected

def test_script_exists_and_executable():
    script_path = "/home/user/prepare_data.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_training_data_exists():
    output_path = "/home/user/training_data.jsonl"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_training_data_contents():
    output_path = "/home/user/training_data.jsonl"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 records in {output_path}, but found {len(lines)}."

    parsed_records = []
    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
            parsed_records.append(record)
        except json.JSONDecodeError:
            assert False, f"Line {i+1} in {output_path} is not valid JSON."

    expected_records = get_expected_data()

    for i in range(5):
        actual = parsed_records[i]
        expected = expected_records[i]

        assert actual.get("id") == expected["id"], f"Record {i+1}: expected id {expected['id']}, got {actual.get('id')}"
        assert actual.get("text") == expected["text"], f"Record {i+1}: expected text {expected['text']}, got {actual.get('text')}"
        assert actual.get("label") == expected["label"], f"Record {i+1}: expected label {expected['label']}, got {actual.get('label')}"
        assert actual.get("embedding") == expected["embedding"], f"Record {i+1}: expected embedding {expected['embedding']}, got {actual.get('embedding')}"