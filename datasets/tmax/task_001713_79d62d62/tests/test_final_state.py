# test_final_state.py

import os
import json
import pytest

def test_cargo_project_exists():
    cargo_toml = "/home/user/etl_cleaner/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"Cargo project not found. Expected {cargo_toml} to exist."

def test_processed_dataset_jsonl():
    output_file = "/home/user/processed_dataset.jsonl"
    assert os.path.isfile(output_file), f"Output file not found at {output_file}."

    expected = [
        {"text": "system is starting", "words": 3, "rolling_avg": 3.00},
        {"text": "processing data batch 1", "words": 4, "rolling_avg": 3.50},
        {"text": "data batch 2 arrived", "words": 4, "rolling_avg": 3.67},
        {"text": "error in pipeline", "words": 3, "rolling_avg": 3.67},
        {"text": "retrying batch 2", "words": 3, "rolling_avg": 3.33},
        {"text": "batch 3 processing", "words": 3, "rolling_avg": 3.00}
    ]

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected), f"Expected {len(expected)} lines in {output_file}, but got {len(lines)}."

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

        assert "text" in data, f"Line {i+1} missing 'text' key."
        assert "words" in data, f"Line {i+1} missing 'words' key."
        assert "rolling_avg" in data, f"Line {i+1} missing 'rolling_avg' key."

        assert data["text"] == expected[i]["text"], f"Line {i+1} text mismatch. Expected '{expected[i]['text']}', got '{data['text']}'"
        assert data["words"] == expected[i]["words"], f"Line {i+1} words mismatch. Expected {expected[i]['words']}, got {data['words']}"

        # Check rolling_avg with tolerance
        actual_avg = float(data["rolling_avg"])
        expected_avg = expected[i]["rolling_avg"]
        assert abs(actual_avg - expected_avg) < 0.015, f"Line {i+1} rolling_avg mismatch. Expected {expected_avg}, got {actual_avg}"