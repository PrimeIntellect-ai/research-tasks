# test_final_state.py

import os
import csv
import pytest

CSV_PATH = '/home/user/top_research.csv'
SCRIPT_PATH = '/home/user/process_results.py'

EXPECTED_CSV_CONTENT = [
    ['TopicName', 'TopPaperTitle', 'TopPaperCitations', 'TopicTotalCitations'],
    ['Artificial Intelligence', 'General AI History', '80', '80'],
    ['Deep Learning', 'CNNs', '1000', '1900'],
    ['Machine Learning', 'Advanced ML', '200', '350'],
    ['Natural Language Processing', 'Attention Mechanisms', '300', '350']
]

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script file {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

def test_csv_exists():
    assert os.path.exists(CSV_PATH), f"Output CSV file {CSV_PATH} does not exist."
    assert os.path.isfile(CSV_PATH), f"{CSV_PATH} is not a file."

def test_csv_content():
    with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        actual_content = list(reader)

    assert actual_content, "The CSV file is empty."

    # Check headers
    assert actual_content[0] == EXPECTED_CSV_CONTENT[0], \
        f"CSV headers are incorrect. Expected {EXPECTED_CSV_CONTENT[0]}, got {actual_content[0]}"

    # Check data rows
    assert len(actual_content) == len(EXPECTED_CSV_CONTENT), \
        f"CSV has incorrect number of rows. Expected {len(EXPECTED_CSV_CONTENT)}, got {len(actual_content)}"

    for i in range(1, len(EXPECTED_CSV_CONTENT)):
        assert actual_content[i] == EXPECTED_CSV_CONTENT[i], \
            f"CSV row {i} is incorrect. Expected {EXPECTED_CSV_CONTENT[i]}, got {actual_content[i]}"