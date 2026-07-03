# test_final_state.py

import os
import pytest
import datetime

EXPECTED_TIMESTAMPS = [
    1697121000,
    1697121060,
    1697121120,
    1697121180,
    1697121240
]

def test_output_csv_row_accuracy():
    output_path = "/home/user/output.csv"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    correct_rows = 0
    for i, line in enumerate(lines):
        if i >= len(EXPECTED_TIMESTAMPS):
            break
        try:
            ts_str, score_str = line.split(',')
            if int(ts_str) == EXPECTED_TIMESTAMPS[i]:
                correct_rows += 1
        except ValueError:
            pass

    row_accuracy = correct_rows / len(EXPECTED_TIMESTAMPS)
    assert row_accuracy >= 0.99, f"row_accuracy={row_accuracy} is below threshold 0.99"

def test_summary_txt_content():
    summary_path = "/home/user/summary.txt"
    assert os.path.exists(summary_path), f"Summary file {summary_path} does not exist."

    with open(summary_path, 'r') as f:
        content = f.read().strip()

    # The accuracy test ensures at least 5 rows are processed successfully if threshold >= 0.99
    expected_text = "Report: Processed 5 valid events."
    assert content == expected_text, f"Summary file content is incorrect. Expected '{expected_text}', got '{content}'"

def test_original_dataset_unmodified():
    dataset_path = "/home/user/data/events.jsonl"
    assert os.path.exists(dataset_path), f"Original dataset {dataset_path} is missing."

    with open(dataset_path, 'r') as f:
        content = f.read()

    assert r"\u0041" in content, "Original dataset was modified (missing \\u0041)"
    assert r"\u26A0" in content, "Original dataset was modified (missing \\u26A0)"
    assert "System boot normal" in content, "Original dataset was modified (missing first line)"