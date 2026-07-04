# test_final_state.py

import os
import json
import pytest

OUTPUT_DIR = "/home/user/output"
CLEAN_DATASET_FILE = os.path.join(OUTPUT_DIR, "clean_dataset.jsonl")
TOP_TOKENS_FILE = os.path.join(OUTPUT_DIR, "top_tokens.txt")

def test_output_directory_exists():
    assert os.path.isdir(OUTPUT_DIR), f"Output directory {OUTPUT_DIR} is missing."

def test_clean_dataset_exists():
    assert os.path.isfile(CLEAN_DATASET_FILE), f"Output file {CLEAN_DATASET_FILE} is missing."

def test_top_tokens_exists():
    assert os.path.isfile(TOP_TOKENS_FILE), f"Output file {TOP_TOKENS_FILE} is missing."

def test_clean_dataset_content():
    expected_doc_ids = [9007199254740993, 9007199254740997, 9007199254740999]
    expected_authors = ["Alice", "Bob", "Carol"]
    expected_texts = [
        "The quick brown fox",
        "hello world from physics the quick",
        "no category text quick"
    ]

    with open(CLEAN_DATASET_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {CLEAN_DATASET_FILE}, found {len(lines)}."

    actual_doc_ids = []

    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {CLEAN_DATASET_FILE} is not valid JSON.")

        assert "doc_id" in record, f"Missing 'doc_id' in line {i+1}."
        assert "author" in record, f"Missing 'author' in line {i+1}."
        assert "category" in record, f"Missing 'category' in line {i+1}."
        assert "text" in record, f"Missing 'text' in line {i+1}."

        # Check doc_id type and value
        doc_id = record["doc_id"]
        # It could be a string if they chose string representation, or exact integer
        if isinstance(doc_id, str):
            assert doc_id.isdigit(), f"'doc_id' string is not an integer in line {i+1}."
            doc_id = int(doc_id)
        else:
            assert isinstance(doc_id, int), f"'doc_id' is not an integer in line {i+1}."

        actual_doc_ids.append(doc_id)

        assert doc_id == expected_doc_ids[i], f"Expected doc_id {expected_doc_ids[i]}, got {doc_id}."
        assert record["author"] == expected_authors[i], f"Expected author {expected_authors[i]}, got {record['author']}."
        assert record["text"] == expected_texts[i], f"Expected text '{expected_texts[i]}', got '{record['text']}'."

        if doc_id == 9007199254740999:
            # Category was missing in CSV
            assert record["category"] in [null, "", None], f"Expected missing category to be null or empty string, got {record['category']}."

def test_top_tokens_content():
    expected_lines = [
        "quick:3",
        "The:1",
        "brown:1"
    ]

    with open(TOP_TOKENS_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {TOP_TOKENS_FILE}, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {TOP_TOKENS_FILE} mismatch. Expected '{expected}', got '{actual}'."