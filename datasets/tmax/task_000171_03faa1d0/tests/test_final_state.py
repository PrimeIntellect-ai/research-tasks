# test_final_state.py
import os
import json
import re
import pytest

RAW_DATA_PATH = "/home/user/raw_data.txt"
CLEAN_DATA_PATH = "/home/user/clean_data.jsonl"
BENCHMARK_PATH = "/home/user/benchmark.txt"

def test_clean_data_jsonl():
    assert os.path.isfile(RAW_DATA_PATH), f"Missing {RAW_DATA_PATH}"
    assert os.path.isfile(CLEAN_DATA_PATH), f"Missing {CLEAN_DATA_PATH}"

    # Derive expected tokens from raw_data.txt
    expected_data = []
    with open(RAW_DATA_PATH, 'r') as f:
        for line in f:
            original_line = line.strip()
            if not original_line:
                continue

            # Filter: contains "AI" and > 5 words
            if "AI" in original_line and len(original_line.split()) > 5:
                # Transform: lowercase, remove punctuation, split
                transformed = original_line.lower()
                for p in ['.', ',', '!', '?']:
                    transformed = transformed.replace(p, '')
                tokens = transformed.split()
                expected_data.append({"tokens": tokens})

    # Read clean_data.jsonl
    actual_data = []
    with open(CLEAN_DATA_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    parsed = json.loads(line)
                    actual_data.append(parsed)
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON in {CLEAN_DATA_PATH}: {line}")

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} lines in {CLEAN_DATA_PATH}, found {len(actual_data)}"

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert "tokens" in actual, f"Line {i+1} missing 'tokens' key"
        assert actual["tokens"] == expected["tokens"], f"Mismatch at line {i+1}. Expected {expected['tokens']}, got {actual['tokens']}"

def test_benchmark_txt():
    assert os.path.isfile(BENCHMARK_PATH), f"Missing {BENCHMARK_PATH}"

    with open(BENCHMARK_PATH, 'r') as f:
        content = f.read().strip()

    pattern = r"^Throughput: \d+\.\d{2} lines/sec$"
    assert re.match(pattern, content), f"Benchmark format incorrect in {BENCHMARK_PATH}. Expected format 'Throughput: X.XX lines/sec', got: '{content}'"