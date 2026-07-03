# test_final_state.py
import os
import json
import pytest

def test_pipeline_output():
    weights_path = "/home/user/weights.tsv"
    raw_data_path = "/home/user/raw_data.jsonl"
    cleaned_data_path = "/home/user/cleaned_data.jsonl"

    assert os.path.exists(weights_path), f"Missing {weights_path}"
    assert os.path.exists(raw_data_path), f"Missing {raw_data_path}"
    assert os.path.exists(cleaned_data_path), f"Missing {cleaned_data_path} - pipeline script may not have run or failed."

    # Read weights
    with open(weights_path, "r") as f:
        line = f.read().strip()
        w_text_str, w_summary_str = line.split('\t')
        w_text = float(w_text_str)
        w_summary = float(w_summary_str)

    # Process raw data to derive expected output
    expected_lines = []
    seen_texts = set()

    with open(raw_data_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Check schema: exactly id, text, summary
            if set(row.keys()) != {"id", "text", "summary"}:
                continue

            # Check types
            if not isinstance(row["id"], int) or isinstance(row["id"], bool):
                continue
            if not isinstance(row["text"], str):
                continue
            if not isinstance(row["summary"], str):
                continue

            # Calculate score
            score = (w_text * len(row["text"])) + (w_summary * len(row["summary"]))
            if not (15.0 <= score <= 100.0):
                continue

            # Deduplication
            if row["text"] in seen_texts:
                continue

            seen_texts.add(row["text"])
            expected_lines.append(row)

    # Read actual output
    actual_lines = []
    with open(cleaned_data_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                actual_lines.append(json.loads(line))
            except json.JSONDecodeError:
                pytest.fail(f"Output file {cleaned_data_path} contains invalid JSON: {line}")

    assert actual_lines == expected_lines, (
        f"Cleaned data does not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )