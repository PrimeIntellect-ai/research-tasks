# test_final_state.py

import os
import json
import pytest

SCRAPED_DATA_PATH = "/home/user/scraped_data.jsonl"
VALID_COUNT_PATH = "/home/user/valid_count.txt"
CLEAN_DATA_PATH = "/home/user/clean_data.jsonl"

@pytest.fixture(scope="module")
def expected_data():
    assert os.path.isfile(SCRAPED_DATA_PATH), f"Original data file {SCRAPED_DATA_PATH} is missing."

    valid_count = 0
    deduped_objects = []
    seen_bodies = set()

    with open(SCRAPED_DATA_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                valid_count += 1
                body = obj.get("body")
                if body not in seen_bodies:
                    seen_bodies.add(body)
                    deduped_objects.append(obj)
            except json.JSONDecodeError:
                pass

    return valid_count, deduped_objects

def test_valid_count_file(expected_data):
    expected_count, _ = expected_data

    assert os.path.isfile(VALID_COUNT_PATH), f"File {VALID_COUNT_PATH} does not exist."

    with open(VALID_COUNT_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content.isdigit(), f"Content of {VALID_COUNT_PATH} is not a valid integer: {content}"
    assert int(content) == expected_count, f"Expected valid count {expected_count}, but got {content}"

def test_clean_data_file(expected_data):
    _, expected_objects = expected_data

    assert os.path.isfile(CLEAN_DATA_PATH), f"File {CLEAN_DATA_PATH} does not exist."

    actual_objects = []
    with open(CLEAN_DATA_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                actual_objects.append(obj)
            except json.JSONDecodeError:
                pytest.fail(f"Line {i+1} in {CLEAN_DATA_PATH} is not valid JSON.")

    assert len(actual_objects) == len(expected_objects), (
        f"Expected {len(expected_objects)} objects in {CLEAN_DATA_PATH}, "
        f"but found {len(actual_objects)}."
    )

    # Sort by ID to ensure order-independent comparison
    expected_sorted = sorted(expected_objects, key=lambda x: x.get("id", 0))
    actual_sorted = sorted(actual_objects, key=lambda x: x.get("id", 0))

    assert actual_sorted == expected_sorted, (
        f"Contents of {CLEAN_DATA_PATH} do not match the expected deduplicated objects."
    )