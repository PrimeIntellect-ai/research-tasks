# test_final_state.py

import os
import json
import pytest

def test_processed_data_exists():
    file_path = "/home/user/processed_data.jsonl"
    assert os.path.exists(file_path), f"Output file {file_path} does not exist. Did you run your Go program?"
    assert os.path.isfile(file_path), f"{file_path} is not a regular file."

def test_processed_data_content():
    file_path = "/home/user/processed_data.jsonl"
    if not os.path.exists(file_path):
        pytest.fail(f"File {file_path} is missing.")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in {file_path}, got {len(lines)}."

    expected_results = {
        1: {
            "text_a": "hallo",
            "text_b": "hello",
            "series": [0.0, 5.0, 10.0],
            "text_distance": 1
        },
        2: {
            "text_a": "こんにちは世界",
            "text_b": "こんちは世界",
            "series": [5.0, 10.0, 15.0, 20.0],
            "text_distance": 1
        },
        3: {
            "text_a": "Привет 🌍",
            "text_b": "Привет 🌎",
            "series": [-1.0, -3.0, -5.0],
            "text_distance": 1
        },
        4: {
            "text_a": "résumé",
            "text_b": "resume",
            "series": [100.0, 125.0, 150.0, 175.0, 200.0],
            "text_distance": 2
        }
    }

    actual_ids = []
    for line in lines:
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON line in {file_path}: {line}")

        assert "id" in data, f"Missing 'id' in record: {data}"
        record_id = data["id"]
        actual_ids.append(record_id)

        assert record_id in expected_results, f"Unexpected id {record_id} found in output."
        expected = expected_results[record_id]

        assert data.get("text_a") == expected["text_a"], f"Incorrect text_a for id {record_id}."
        assert data.get("text_b") == expected["text_b"], f"Incorrect text_b for id {record_id}."

        # Check series
        actual_series = data.get("series")
        assert actual_series is not None, f"Missing 'series' for id {record_id}."
        assert len(actual_series) == len(expected["series"]), f"Incorrect series length for id {record_id}."
        for act, exp in zip(actual_series, expected["series"]):
            assert act is not None, f"Found null in series for id {record_id}."
            assert abs(act - exp) < 1e-6, f"Incorrect series value for id {record_id}: expected {exp}, got {act}."

        # Check distance
        actual_distance = data.get("text_distance")
        assert actual_distance is not None, f"Missing 'text_distance' for id {record_id}."
        assert actual_distance == expected["text_distance"], f"Incorrect text_distance for id {record_id}: expected {expected['text_distance']}, got {actual_distance}."

    assert sorted(actual_ids) == [1, 2, 3, 4], "Missing some expected ids in the output."